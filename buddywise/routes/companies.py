from flask import Blueprint, abort, jsonify, make_response

from buddywise.exceptions import AccessLayerException
from buddywise.models.access_layers.company_access_layer import CompanyAccessLayer
from buddywise.services.company_service import CompanyService

company_urls = Blueprint("company_urls", __name__, url_prefix="/company")


@company_urls.route("/", methods=["GET"])
def list_companies():
    """
    Returns a list of company ids.

    Returns:
    A dictionary containing a list of company ids under the key "companies".
    """
    company_ids = CompanyService.get_company_ids()
    return {"companies": company_ids}, 200


@company_urls.route("/<company_id>", methods=["GET"])
def get_company_name(company_id: str):
    """
    Retrieves the name of the company with the given ID.

    Args:
        company_id (str): The ID of the company.

    Returns:
        A dictionary with the name of the company under the "name" key.

    Raises:
        HTTPException (404): If the company with the given ID is not found.
    """
    try:
        company = CompanyAccessLayer.get_company_by_guid(guid=company_id)
        return {"name": company.name}, 200
    except AccessLayerException:
        abort(make_response(jsonify(success=False, message="not found"), 404))


@company_urls.route("/<company_id>/employees", methods=["GET"])
def list_employees(company_id: str):
    """
    List employees of a company.

    Args:
    company_id (str): The ID of the company whose employees are to be listed.

    Returns:
    A tuple containing a dictionary of employee IDs and a HTTP status code 200 indicating success.

    Raises:
    None.
    """
    emp_ids = CompanyService.get_company_employees(guid=company_id)
    return {"employees": emp_ids}, 200
