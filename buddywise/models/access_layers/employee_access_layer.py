from typing import List

from mongoengine import DoesNotExist

from buddywise.exceptions import AccessLayerException
from buddywise.models.employee import Employee


class EmployeeAccessLayer:
    """
    A class for accessing employee data using MongoDB and mongoengine.
    """

    @staticmethod
    def get_employee_by_guid(guid: str):
        """
        Get an employee by GUID.

        Parameters:
            guid (str): The GUID of the employee to retrieve.

        Returns:
            Employee: The employee with the specified GUID.

        Raises:
            AccessLayerException: If no employee with the specified GUID is found.
        """
        try:
            return Employee.objects.get(guid=guid)
        except DoesNotExist:
            raise AccessLayerException

    @staticmethod
    def get_alive_employees_by_eye_color(guids: List, eye_color: str) -> List[Employee]:
        """
        Get all the alive employees with a specified eye color and whose GUIDs are in the specified list.

        Parameters:
            guids (List): A list of GUIDs to filter by.
            eye_color (str): The eye color to filter by.

        Returns:
            List[Employee]: A list of alive employees that match the specified criteria.
        """
        return list(
            Employee.objects.filter(guid__in=guids, eye_color=eye_color, has_died=False)
        )

    @staticmethod
    def get_employees_by_company_id(company_id: str) -> List[Employee]:
        return list(Employee.objects.filter(company_id=company_id))
