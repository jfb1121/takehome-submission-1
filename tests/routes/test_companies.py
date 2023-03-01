from buddywise.models.company import Company
from buddywise.models.employee import Employee


class TestCompanies:
    BASE_URL = "/company/"
    def test_get_company_employees(self, client, db, tear_downdb):
        Company(guid="1",
                name="foo").save()
        Company(guid="2",
                name="bar").save()

        res = client.get(self.BASE_URL)
        assert res.json["companies"] == ["1", "2"]

        tear_downdb()

    def test_get_company_name(self, client, db, tear_downdb):
        Company(guid="1",
                name="foo").save()
        res = client.get(f"{self.BASE_URL}1")

        assert res.json["name"] == "foo"
        tear_downdb()

    def test_list_employees(self, client, db, tear_downdb):
        Company(guid="1",
                name="foo").save()
        Employee(
            guid="1",
            has_died=False,
            company_id="1"
        ).save()
        Employee(
            guid="2",
            has_died=False,
            company_id="1"
        ).save()

        res = client.get(f"{self.BASE_URL}1/employees")
        assert res.json["employees"] == ["1", "2"]

        tear_downdb()




