from django.db import models, transaction
from django.utils import translation


_ = translation.gettext_lazy


class StatusMixin(models.Model):
    """ Base for status mixin used in sales order, warehouse transfer or invoice """

    class Meta:
        abstract = True

    TRASH = 'trash'
    DRAFT = 'draft'
    VALID = 'valid'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PROCESS = 'process'
    COMPLETE = 'complete'
    CLOSED = 'closed'
    STATUS = (
        (TRASH, _('Trash')),
        (DRAFT, _('Draft')),
        (VALID, _('Valid')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (PROCESS, _('Process')),
        (COMPLETE, _('Complete')),
        (CLOSED, _('Closed')),
    )

    status = models.CharField(
        choices=STATUS, default=DRAFT,
        max_length=15,
        verbose_name=_('Status'))

    @property
    def is_draft(self):
        """ Check order status is draft """
        return self.status == 'draft'

    @property
    def is_trash(self):
        """ Check order status is trashed """
        return self.status == 'trash'

    @property
    def is_valid(self):
        """ Check order status is valid """
        return self.status == 'valid'

    @property
    def is_approved(self):
        """ Check order status is approved """
        return self.status == 'approved'

    @property
    def is_rejected(self):
        """ Check order status is rejected """
        return self.status == 'rejected'

    @property
    def is_processed(self):
        """ Check order status is processed """
        return self.status == 'process'

    @property
    def is_completed(self):
        """ Check order status is completed """
        return self.status == 'complete'

    @property
    def is_closed(self) -> bool:
        """ Check order status is closed """
        return self.status == 'closed'

    @property
    def is_editable(self) -> bool:
        """ Check order is editable """
        return self.is_trash or self.is_draft

    def draft(self):
        """ Draft trashed """
        if self.is_draft:
            return
        if self.is_trash:
            self.status = 'draft'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be draft.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def trash(self):
        """ Trash drafted order """
        if self.is_trash:
            return
        if self.is_draft:
            self.status = 'trash'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be trash.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def clean_validate_action(self):
        pass

    @transaction.atomic
    def validate(self):
        """ Validate drafted order """
        if self.is_valid:
            return
        if self.is_draft:
            self.clean_validate_action()
            self.status = 'valid'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be validated")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))


class ThreeStepStatusMixin(StatusMixin):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> complete
    """

    class Meta:
        abstract = True

    def clean_complete_action(self):
        pass

    @transaction.atomic
    def complete(self):
        """ Complete validated order """
        if getattr(self, 'is_completed'):
            return
        if getattr(self, 'is_valid'):
            self.clean_complete_action()
            self.status = 'complete'
            self.save()
        else:
            msg = _("{} {} is {}, it can't be completed.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))


class FourStepStatusMixin(StatusMixin):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> process -> complete
    """

    class Meta:
        abstract = True

    def clean_process_action(self):
        pass

    @transaction.atomic
    def process(self):
        """ Process valid order """
        if getattr(self, 'is_processed'):
            return
        if getattr(self, 'is_valid'):
            self.clean_process_action()
            self.status = 'process'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be processed.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def clean_complete_action(self):
        pass

    @transaction.atomic
    def complete(self):
        """ Complete validated order """
        if getattr(self, 'is_completed'):
            return
        if getattr(self, 'is_processed'):
            self.clean_complete_action()
            self.status = 'complete'
            self.save()
        else:
            msg = _("{} {} is {}, it can't be completed.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))


class FiveStepStatusMixin(StatusMixin):
    """ Give model status three step status tracking and action,
        draft -> validate or trash -> approve/reject -> process -> complete
    """

    class Meta:
        abstract = True

    def clean_approve_action(self):
        pass

    @transaction.atomic
    def approve(self):
        """ Approve valid order """
        if getattr(self, 'is_approved'):
            return
        if getattr(self, 'is_valid'):
            self.clean_approve_action()
            self.status = 'approved'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be approved.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def clean_reject_action(self):
        pass

    @transaction.atomic
    def reject(self):
        """ Reject valid order """
        if getattr(self, 'is_approved') or getattr(self, 'is_rejected'):
            return
        if getattr(self, 'is_valid'):
            self.clean_reject_action()
            self.status = 'rejected'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be rejected.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def clean_process_action(self):
        pass

    @transaction.atomic
    def process(self):
        """ Process approved order """
        if getattr(self, 'is_processed'):
            return
        if getattr(self, 'is_approved'):
            self.clean_process_action()
            self.status = 'process'
            self.save()
        else:
            msg = _("{} #{} is {}, it can't be processed.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))

    def clean_complete_action(self):
        pass

    @transaction.atomic
    def complete(self):
        """ Complete validated order """
        if getattr(self, 'is_completed'):
            return
        if getattr(self, 'is_processed'):
            self.clean_complete_action()
            self.status = 'complete'
            self.save()
        else:
            msg = _("{} {} is {}, it can't be completed.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))


class CloseStatusMixin(models.Model):
    class Meta:
        abstract = True

    def close(self):
        """ Close the order """
        if getattr(self, 'is_closed'):
            return
        if getattr(self, 'is_completed'):
            self.status = 'closed'
            self.save()
        else:
            msg = _("{} {} is {}, it can't be finished.")
            raise PermissionError(
                str(msg).format(self._meta.verbose_name, self.inner_id, self.status))
