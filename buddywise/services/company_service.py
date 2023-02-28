from typing import List

from buddywise.models.access_layers.company_access_layer import CompanyAccessLayer
from buddywise.models.access_layers.employee_access_layer import EmployeeAccessLayer


class CompanyService:
    """
    A service class for handling company-related operations.
    """

    @staticmethod
    def get_company_employees(guid: str) -> List[str]:
        """
        Returns a list of employee IDs for a given company.

        Args:
            guid (str): The ID of the company.

        Returns:
            list: A list of employee IDs.
        """
        emps = EmployeeAccessLayer.get_employees_by_company_id(company_id=guid)
        emp_ids = [emp.guid for emp in emps]

        return emp_ids

    @staticmethod
    def get_company_ids():
        """
        Returns a list of company IDs.

        Returns:
            list: A list of company IDs.
        """
        companies = CompanyAccessLayer.get_all_companies()
        return [comp.guid for comp in companies]
