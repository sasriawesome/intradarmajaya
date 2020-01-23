from django.contrib.auth.models import Permission


def apply_create_wh_group(apps, schema_editor):
    """ Create Warehouse Groups """
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Warehouse Users'),
        Group(name=u'Warehouse Staffs'),
        Group(name=u'Warehouse Supervisors'),
        Group(name=u'Warehouse Managers'),
        Group(name=u'Warehouse Admins'),
    ])


def revert_create_wh_group(apps, schema_editor):
    """ Delete Warehouse Groups """
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=[
        u'Warehouse Users',
        u'Warehouse Staffs',
        u'Warehouse Supervisors',
        u'Warehouse Managers',
        u'Warehouse Admins'
    ]).delete()


def apply_create_wh_group_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    wh_users, created = Group.objects.get_or_create(name=u'Warehouse Users')
    wh_staffs, created = Group.objects.get_or_create(name=u'Warehouse Staffs')
    wh_supervisors, created = Group.objects.get_or_create(name=u'Warehouse Supervisors')
    wh_managers, created = Group.objects.get_or_create(name=u'Warehouse Managers')
    wh_admins, created = Group.objects.get_or_create(name=u'Warehouse Admins')

    wh_users_perms = Permission.objects.filter(codename__in=[
        'access_admin',

        'view_requestorder',
        'add_requestorder',
        'change_requestorder',
        'trash_requestorder',
        'draft_requestorder',
        'validate_requestorder',
        'print_requestorder',
    ])

    wh_staffs_perms = Permission.objects.filter(codename__in=[
        'access_admin',

        'view_stockcard',

        'add_inventory',
        'change_inventory',
        'view_inventory',

        'add_asset',
        'change_asset',
        'view_asset',

        'add_warehouselocation',
        'change_warehouselocation',
        'view_warehouselocation',

        'add_productcategory',
        'change_productcategory',
        'view_productcategory',

        'add_unitofmeasure',
        'change_unitofmeasure',
        'view_unitofmeasure',

        'view_requestorder',
        'viewother_requestorder',
        'process_requestorder',
        'print_requestorder',

        'add_stockadjustment',
        'change_stockadjustment',
        'view_stockadjustment',
        'validate_stockadjustment',
        'reconcile_stockadjustment',
        'print_stockadjustment',

        'add_transfercheckin',
        'change_transfercheckin',
        'view_transfercheckin',
        'trash_transfercheckin',
        'draft_transfercheckin',
        'validate_transfercheckin',
        'process_transfercheckin',
        'complete_transfercheckin',
        'print_transfercheckin',

        'add_transfercheckout',
        'change_transfercheckout',
        'view_transfercheckout',
        'trash_transfercheckout',
        'draft_transfercheckout',
        'validate_transfercheckout',
        'process_transfercheckout',
        'complete_transfercheckout',
        'print_transfercheckout',

        'add_transferscrapped',
        'change_transferscrapped',
        'view_transferscrapped',
        'trash_transferscrapped',
        'draft_transferscrapped',
        'validate_transferscrapped',
        'process_transferscrapped',
        'complete_transferscrapped',
        'print_transferscrapped',
    ])

    wh_supervisors_perms = Permission.objects.filter(codename__in=[
        'access_admin',

        'add_inventory',
        'change_inventory',
        'view_inventory',

        'add_asset',
        'change_asset',
        'view_asset',

        'add_location',
        'change_location',
        'view_location',

        'add_productcategory',
        'change_productcategory',
        'view_productcategory',

        'add_unitofmeasure',
        'change_unitofmeasure',
        'view_unitofmeasure',

        'view_requestorder',
        'viewother_requestorder',
        'process_requestorder',
        'print_requestorder',

        'complete_requestorder',
        'close_requestorder',
    ])

    wh_managers_perms = Permission.objects.filter(codename__in=[
        'access_admin',
        'view_location',
        'view_inventory',
        'view_asset',
        'view_stockcard',
        'view_productcategory',
        'view_unitofmeasure',
        'view_partner',
        'view_supplier',

        'view_requestorder',
        'viewother_requestorder',
        'approve_requestorder',
        'reject_requestorder',

        'view_transfercheckin',
        'view_transfercheckout',
        'view_transferscrapped',
    ])

    wh_admins_perms = Permission.objects.filter(codename__in=[

        'access_admin',

        'add_inventory',
        'change_inventory',
        'view_inventory',

        'add_asset',
        'change_asset',
        'view_asset',

        'add_location',
        'change_location',
        'view_location',

        'add_productcategory',
        'change_productcategory',
        'view_productcategory',

        'add_unitofmeasure',
        'change_unitofmeasure',
        'view_unitofmeasure',

        'view_requestorder',
        'viewother_requestorder',
        'add_requestorder',
        'change_requestorder',
        'trash_requestorder',
        'draft_requestorder',
        'validate_transfercheckout',
        'process_requestorder',
        'approve_requestorder',
        'reject_requestorder',
        'complete_requestorder',
        'close_requestorder',
        'print_requestorder',

        'add_stockadjustment',
        'change_stockadjustment',
        'view_stockadjustment',
        'validate_stockadjustment',
        'reconcile_stockadjustment',
        'print_stockadjustment',

        'add_transfercheckin',
        'change_transfercheckin',
        'view_transfercheckin',
        'trash_transfercheckin',
        'draft_transfercheckin',
        'validate_transfercheckin',
        'process_transfercheckin',
        'complete_transfercheckin',
        'print_transfercheckin',

        'add_transfercheckout',
        'change_transfercheckout',
        'view_transfercheckout',
        'trash_transfercheckout',
        'draft_transfercheckout',
        'validate_transfercheckout',
        'process_transfercheckout',
        'complete_transfercheckout',
        'print_transfercheckout',

        'add_transferscrapped',
        'change_transferscrapped',
        'view_transferscrapped',
        'trash_transferscrapped',
        'draft_transferscrapped',
        'validate_transferscrapped',
        'process_transferscrapped',
        'complete_transferscrapped',
        'print_transferscrapped',
    ])

    wh_users.permissions.set(wh_users_perms, clear=True)
    wh_staffs.permissions.set(wh_staffs_perms, clear=True)
    wh_supervisors.permissions.set(wh_supervisors_perms, clear=True)
    wh_managers.permissions.set(wh_managers_perms, clear=True)
    wh_admins.permissions.set(wh_admins_perms, clear=True)


def revert_create_wh_group_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    wh_users = Group.objects.get(name=u'Warehouse Users')
    wh_users.permissions.clear()

    wh_staffs = Group.objects.get(name=u'Warehouse Staffs')
    wh_staffs.permissions.clear()

    wh_supervisors = Group.objects.get(name=u'Warehouse Supervisors')
    wh_supervisors.permissions.clear()

    wh_managers = Group.objects.get(name=u'Warehouse Managers')
    wh_managers.permissions.clear()

    wh_admins = Group.objects.get(name=u'Warehouse Admins')
    wh_admins.permissions.clear()
