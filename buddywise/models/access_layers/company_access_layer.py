from typing import List, Optional

from mongoengine import DoesNotExist

from buddywise.exceptions import AccessLayerException
from buddywise.models.company import Company


class CompanyAccessLayer:
    """
    Class responsible to abstract all the database logic.
    """

    @staticmethod
    def get_company_by_guid(guid: str) -> Optional[Company]:
        """
        fetches a company by guid.

        Parameters:
            guid (str): GUID of the company to fetch.

        Returns:
            Optional[Company]: The company object if it exists, None otherwise.

        Raises:
            AccessLayerException: If the company with the given GUID doesn't exist.
        """
        try:
            return Company.objects.get(guid=guid)
        except DoesNotExist:
            raise AccessLayerException

    @staticmethod
    def get_all_companies() -> List[Company]:
        """
        Fetches all companies from the database.

        Returns:
            list[Company]: A list of all the company objects in the database.
        """
        print(f"----------------------{list(Company.objects())}")
        return list(Company.objects())
