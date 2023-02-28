from buddywise.exceptions import AccessLayerException, ServiceException
from buddywise.models.access_layers.company_access_layer import CompanyAccessLayer
from buddywise.models.access_layers.employee_access_layer import EmployeeAccessLayer
from buddywise.models.employee import Employee


class EmployeeService:
    """
    A service class for handling employee-related operations.

    Attributes:
        FRUITS (list): A list of fruits.
        VEGETABLES (list): A list of vegetables.
    """

    FRUITS = ["apple", "banana", "orange", "strawberry"]
    VEGETABLES = ["beetroot", "carrot", "celery", "cucumber"]

    @staticmethod
    def get_common_friends(emp_1: Employee, emp_2: Employee):
        """
        Returns a list of common friends between two employees.

        Args:
            emp_1 (Employee): The first employee object.
            emp_2 (Employee): The second employee object.

        Returns:
            list: A list of common friends' IDs.
        """
        emp_1_friends = emp_1.friends
        emp_2_friends = emp_2.friends
        if emp_1.guid in emp_1_friends:
            emp_1_friends.remove(emp_1.guid)

        if emp_2.guid in emp_2_friends:
            emp_2_friends.remove(emp_2.guid)

        common_friends = set(emp_1_friends).intersection(set(emp_2_friends))

        return list(common_friends)

    def get_employees_and_common_friends(self, employee_id: str, employee_2_id: str):
        """
        Returns employee details and their common friends with brown eyes.

        Args:
            employee_id (str): The ID of the first employee.
            employee_2_id (str): The ID of the second employee.

        Raises:
            ServiceException: If both employees have the same ID.

        Returns:
            dict: A dictionary containing employee details and their common friends.
        """
        if employee_id == employee_2_id:
            raise ServiceException("both employees can't be the same")

        emp_1 = EmployeeAccessLayer.get_employee_by_guid(guid=employee_id)
        emp_2 = EmployeeAccessLayer.get_employee_by_guid(guid=employee_2_id)
        common_friends = self.get_common_friends(emp_1, emp_2)
        alive_friends_with_brown_eyes = (
            EmployeeAccessLayer.get_alive_employees_by_eye_color(
                guids=common_friends, eye_color="brown"
            )
        )
        alive_friends_with_brown_eyes = [
            emp.guid for emp in alive_friends_with_brown_eyes
        ]

        output = {
            "employee_details": {
                employee_id: {
                    "Name": emp_1.name,
                    "Age": emp_1.age,
                    "Phone": emp_1.phone,
                    "Address": emp_1.address,
                },
                employee_2_id: {
                    "Name": emp_2.name,
                    "Age": emp_2.age,
                    "Phone": emp_2.phone,
                    "Address": emp_2.address,
                },
            },
            "common_friends": alive_friends_with_brown_eyes,
        }

        return output

    def get_employee_details(self, employee_id: str):
        """
        Returns details of a specific employee.

        Args:
            employee_id (str): The ID of the employee.

        Returns:
            dict: A dictionary containing employee details.
        """
        emp = EmployeeAccessLayer.get_employee_by_guid(guid=employee_id)
        company = CompanyAccessLayer.get_company_by_guid(guid=emp.company_id)

        output = {
            "name": emp.name,
            "age": emp.age,
            "company": company.name,
            "fruits": sorted(
                list(set(self.FRUITS).intersection(set(emp.favourite_food)))
            ),
            "vegetables": sorted(
                list(set(self.VEGETABLES).intersection(set(emp.favourite_food)))
            ),
        }

        return output
