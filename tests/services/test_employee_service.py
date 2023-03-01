from unittest.mock import MagicMock, patch

from buddywise.models.access_layers.company_access_layer import CompanyAccessLayer
from buddywise.models.access_layers.employee_access_layer import EmployeeAccessLayer
from buddywise.models.employee import Employee
from buddywise.services.employee_service import EmployeeService


class TestEmployeeService:
    @patch("buddywise.services.employee_service.EmployeeAccessLayer")
    def test_get_employees_and_common_friends(self, mock_employee_access_layer):
        # Create mock data
        emp_1 = Employee(
            guid="1",
            has_died=False,
            company_id="1",
            age="30",
            friends=["2", "3", "8"],
            address="123 Main St",
            phone="1234567890",
            name="John",
        )
        emp_2 = Employee(
            guid="2",
            has_died=False,
            company_id="1",
            age="25",
            friends=["3", "4", "5"],
            address="456 Elm St",
            phone="9876543210",
            name="Jane",
        )
        common_friends = ["3"]
        alive_friends_with_brown_eyes = [
            Employee(
                guid="3",
                name="Tom",
                company_id="1",
                age=28,
                phone="1112223333",
                address="789 Oak St",
            )
        ]

        # Set up mock return values for EmployeeAccessLayer methods
        mock_employee_access_layer.get_employee_by_guid.side_effect = [emp_1, emp_2]
        mock_employee_access_layer.get_common_friends.return_value = common_friends
        mock_employee_access_layer.get_alive_employees_by_eye_color.return_value = (
            alive_friends_with_brown_eyes
        )

        # Call the function and check the output
        employee_service = EmployeeService()
        output = employee_service.get_employees_and_common_friends("1", "2")

        assert output == {
            "employee_details": {
                "1": {
                    "Name": "John",
                    "Age": 30,
                    "Phone": "1234567890",
                    "Address": "123 Main St",
                },
                "2": {
                    "Name": "Jane",
                    "Age": 25,
                    "Phone": "9876543210",
                    "Address": "456 Elm St",
                },
            },
            "common_friends": ["3"],
        }

    @patch.object(EmployeeAccessLayer, "get_employee_by_guid")
    @patch.object(CompanyAccessLayer, "get_company_by_guid")
    def test_get_employee_details(
        self, mock_company_access_layer, mock_employee_access_layer, db, tear_downdb
    ):
        employee_service = EmployeeService()
        mock_emp = MagicMock(spec=Employee)
        mock_emp.guid = "123"
        mock_emp.name = "John Smith"
        mock_emp.age = 25
        mock_emp.favourite_food = ["apple", "banana", "carrot"]
        mock_emp.company_id = "456"
        mock_company = MagicMock()
        mock_company.name = "ACME Inc."
        mock_employee_access_layer.return_value = mock_emp
        mock_company_access_layer.return_value = mock_company

        expected_output = {
            "name": "John Smith",
            "age": 25,
            "company": "ACME Inc.",
            "fruits": ["apple", "banana"],
            "vegetables": ["carrot"],
        }

        assert employee_service.get_employee_details("123") == expected_output
        mock_employee_access_layer.assert_called_once_with(guid="123")
        mock_company_access_layer.assert_called_once_with(guid="456")
        tear_downdb()
