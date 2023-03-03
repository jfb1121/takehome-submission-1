import json
from typing import Any, Dict
from uuid import uuid4

from dateutil import parser
from mongoengine import connect

from buddywise.models.company import Company
from buddywise.models.employee import Employee


def load_file(file_name: str) -> Any:
    with open(file_name) as f:
        file_data = json.load(f)

    return file_data


def load_company_data():
    guid_index_map = {}
    company_data = load_file("companies.json")
    for company in company_data:
        guid = str(uuid4())
        Company(guid=guid, name=company["company"]).save()
        guid_index_map[company["index"]] = guid

    return guid_index_map


def replace_index_with_guids(employee_data: list, index_guid_map: dict):
    for emp in employee_data:
        friends = []
        for friend in emp["friends"]:
            friends.append(index_guid_map[friend["index"]])
        emp["friends"] = friends
    return employee_data


def load_employee_data(company_index_id: dict):
    index_guid_map = {}
    employee_data = load_file("people.json")
    for emp in employee_data:
        index_guid_map[emp["index"]] = emp["guid"]
    employee_data = replace_index_with_guids(employee_data, index_guid_map)

    for emp in employee_data:
        emp["company_id"] = company_index_id.get(
            emp["company_id"], str(uuid4())
        )  # index 100 doesn't exist in company.
        emp["eye_color"] = emp.pop("eyeColor")
        emp["favourite_food"] = emp.pop("favouriteFood")
        emp["registered"] = parser.parse(emp["registered"])
        emp.pop("picture")
        emp.pop("index")
        emp.pop("_id")
        Employee(**emp).save()


if __name__ == "__main__":
    # ideally should come from config / env variables.
    connect(
        db="assignment",
        host="127.0.0.1",
        port=27017,
        username="admin",
        password="password",
    )
    guid_index_map = load_company_data()
    load_employee_data(guid_index_map)
