from auth.rbac import get_role_level, has_permission


def test_role_levels():
    assert get_role_level("Intern") == 1
    assert get_role_level("Manager") == 2
    assert get_role_level("HR Admin") == 3
    assert get_role_level("System Admin") == 4


def test_intern_permissions():
    assert has_permission("Intern", "Public") is True
    assert has_permission("Intern", "Payroll") is False


def test_manager_permissions():
    assert has_permission("Manager", "Internal") is True
    assert has_permission("Manager", "Payroll") is False


def test_hr_admin_permissions():
    assert has_permission("HR Admin", "Payroll") is True


def test_system_admin_permissions():
    assert has_permission("System Admin", "System") is True