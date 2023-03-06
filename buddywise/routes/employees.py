from flask import Blueprint, request, abort, make_response, jsonify

from buddywise.exceptions import AccessLayerException
from buddywise.services.employee_service import EmployeeService

employee_urls = Blueprint("employees_urls", __name__, url_prefix="/employee")


@employee_urls.route("/get-common-friends", methods=["GET"])
def get_common_friends():
    """
    Returns common friends between two employees.

    Query Parameters:
        emp1_id (str): The ID of the first employee.
        emp2_id (str): The ID of the second employee.

    Returns:
        dict: A dictionary containing the employee details and a list of common friends.
    """
    emp1_id = request.args.get("emp1_id", "")
    emp2_id = request.args.get("emp2_id", "")
    data = EmployeeService().get_employees_and_common_friends(
        employee_id=emp1_id, employee_2_id=emp2_id
    )
    return data, 200


@employee_urls.route("/<employee_id>", methods=["GET"])
def get_employee_details(employee_id: str):
    """
    Returns details of an employee.

    Args:
        employee_id (str): The ID of the employee.

    Returns:
        dict: A dictionary containing the employee details.
    """
    try:
        data = EmployeeService().get_employee_details(employee_id=employee_id)
        return data, 200
    except AccessLayerException:
        abort(make_response(jsonify(success=False, message="not found"), 404))

