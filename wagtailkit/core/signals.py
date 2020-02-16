import django.dispatch

post_validated = django.dispatch.Signal(providing_args=["instance"])
post_approved = django.dispatch.Signal(providing_args=["instance"])
post_rejected = django.dispatch.Signal(providing_args=["instance"])
post_processed = django.dispatch.Signal(providing_args=["instance"])
post_completed = django.dispatch.Signal(providing_args=["instance"])