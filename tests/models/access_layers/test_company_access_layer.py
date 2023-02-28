import pytest

from buddywise.exceptions import AccessLayerException
from buddywise.models.access_layers.company_access_layer import CompanyAccessLayer
from buddywise.models.company import Company


class TestCompanyAccessLayer:
    def test_get_company_by_guid(self, db, tear_downdb):
        # setup
        guid = "test_guid"
        name = "foobar"
        Company(guid=guid, name=name).save()

        company = CompanyAccessLayer().get_company_by_guid(guid=guid)
        assert company.name == name
        tear_downdb()

    def test_get_company_by_guid_raises(self, db, tear_downdb):
        # setup
        guid = "test_guid"
        with pytest.raises(AccessLayerException):
            company = CompanyAccessLayer().get_company_by_guid(guid=guid)
        tear_downdb()

    def test_get_all_companies(self, db, tear_downdb):
        companies = CompanyAccessLayer().get_all_companies()
        assert companies == []
        for i in range(5):
            Company(guid=str(i), name=str(i)).save()

        companies = CompanyAccessLayer().get_all_companies()
        assert len(companies) == 5
        assert companies[0].guid == str(0)

        tear_downdb()
