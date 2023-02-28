from buddywise.models.access_layers.employee_access_layer import EmployeeAccessLayer
from buddywise.models.employee import Employee


class TestEmployeeAccessLayer:
    def test_get_employees_by_company_id(self, db, tear_downdb):
        pass

    def test_get_alive_employees_by_eye_color(self, db, tear_downdb):
        employees = EmployeeAccessLayer.get_alive_employees_by_eye_color(
            guids=["1"], eye_color="brown"
        )
        assert employees == []

        Employee(guid="1", has_died=False, eye_color="brown", company_id="foo").save()
        Employee(guid="2", has_died=True, eye_color="brown", company_id="foo").save()
        employees = EmployeeAccessLayer.get_alive_employees_by_eye_color(
            guids=["1", "2"], eye_color="brown"
        )
        assert len(employees) == 1
        assert employees[0].guid == "1"
        tear_downdb()
