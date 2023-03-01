from buddywise.models.company import Company
from buddywise.models.employee import Employee


class TestEmployees:
    BASE_URL = "/employee"

    def test_get_common_friends(self, client, db, tear_downdb):
        emp_1 = Employee(
            guid="1",
            has_died=False,
            company_id="1",
            age="30",
            friends=["2", "3", "8"],
            address="123 Main St",
            phone="1234567890",
            name="John",
        ).save()
        emp_2 = Employee(
            guid="2",
            has_died=False,
            company_id="1",
            age="25",
            friends=["3", "4", "5"],
            address="456 Elm St",
            phone="9876543210",
            name="Jane",
        ).save()
        Employee(
            guid="3",
            name="Tom",
            company_id="1",
            age=28,
            phone="1112223333",
            address="789 Oak St",
            eye_color="brown",
            has_died=False,
        ).save()

        query_string = {"emp1_id": 1, "emp2_id": 2}

        res = client.get(
            f"{self.BASE_URL}/get-common-friends", query_string=query_string
        )
        assert res.json == {
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

        tear_downdb()

    def test_get_employee_details(self, client, db, tear_downdb):
        emp_1 = Employee(
            guid="1",
            has_died=False,
            company_id="1",
            age="30",
            friends=["2", "3", "8"],
            address="123 Main St",
            phone="1234567890",
            name="John",
            favourite_food=["apple", "banana", "carrot"],
        ).save()
        Company(guid="1", name="foo").save()
        res = client.get(f"{self.BASE_URL}/1")
        assert res.json == {
            "name": "John",
            "age": 30,
            "company": "foo",
            "fruits": ["apple", "banana"],
            "vegetables": ["carrot"],
        }
