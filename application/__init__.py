import json
from builtins import FileNotFoundError
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from application.service_clients.esec import make_esec_client
from application.service_clients.esec.implementation import EsecException
from application.service_clients.register_adapter import make_register_adapter_client
from application.service_clients.title_adaptor import make_title_adaptor_client

import os
import logging
from logger import logging_config

logging_config.setup_logging()
LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting the server")


app = Flask(__name__, static_folder="static")

db = SQLAlchemy(app)

from .borrower.model import DatabaseException  # noqa

esec_client = make_esec_client()

# Register routes after establishing the db prevents improperly loaded modules
# caused from circular imports
from .deed.views import deed_bp  # noqa
from .borrower.views import borrower_bp  # noqa
from .casework.views import casework_bp  # noqa

app.config.from_pyfile("config.py")
app.register_blueprint(deed_bp, url_prefix="/deed")
app.register_blueprint(borrower_bp, url_prefix="/borrower")
app.register_blueprint(casework_bp, url_prefix="/casework")
app.url_map.strict_slashes = False


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.route("/health")
def check_status():

    return json.dumps({
        "Status": "OK",
        "headers": str(request.headers),
        "commit": str(os.getenv("COMMIT", "LOCAL"))
    })


@app.route("/health/service-check")
def service_check_routes():

    service_list = {
        "services":
        [

        ]
    }

    # Test the deeds database; try and connect to it and retrieve the version value
    try:
        # Attempt to retrieve the value of the alembic version
        # from the relevant deed_api table
        result = db.engine.execute("SELECT version_num FROM alembic_version;")

        rowResults = []

        for row in result:
            rowResults.append(row[0])

        # If the above statement passes, we can assume that a connection
        # to the database has been established.
        # If an exception occurs whilst retrieving the result, then the service
        # will not reach this point.
        service_list["services"].append(get_service_check_dict(200, "deed-api", "postgres deeds (db)",
                                                               "Successfully connected", rowResults[0]))

    except Exception as e:
        # If we have found an exception, then we can presume the connection to the database did not work
        app.logger.error("Database Exception: %s", (e,), exc_info=True)

        service_list["services"].append(get_service_check_dict(500, "deed-api", "postgres deeds (db)",
                                                               "A database exception has occurred"))

    # Attempt to connect to the esec client and append the result to the service list
    esec_service_dict = get_service_check_response("deed-api", "esec-client", "esec")
    service_list["services"].append(esec_service_dict)

    # Attempt to connect to the title adapter (stub(local) or api(live))
    # and add the two results to the service list
    service_list = get_multiple_dict_values("deed-api", "title adapter stub/api",
                                            "title", service_list)

    # Attempt to connect to the register adapter (stub(local) or api(live))
    # and add the two results to the service list
    service_list = get_multiple_dict_values("deed-api", "register-adapter (stub if local)",
                                            "register", service_list)

    return json.dumps(service_list)


def get_service_check_response(service_from, service_to, interface_name):

    # Attempt to connect to a specific service
    service_response = ""
    service_dict = ""

    try:
        # Retrieve the json response from external services
        if interface_name == "esec":
            esec_interface = make_esec_client()
            service_response = esec_interface.check_service_health()
        elif interface_name == "title":
            title_interface = make_title_adaptor_client()
            service_response = title_interface.check_service_health()
        elif interface_name == "register":
            register_interface = make_register_adapter_client()
            service_response = register_interface.check_service_health()

        # Change the json into a dict format
        service_dict = json.loads(service_response.text)

    # If a 500 error is reported, it will be far easier to determine the cause by
    # throwing an exception, rather than by getting an "unexpected error"
    except Exception as e:
        # A RequestException resolves the error that occurs when a connection cant be established
        # and the ValueError/TypeError exception may occur if the dict string / object is malformed
        app.logger.error("An exception has occurred in the service-check route: %s", (e,), exc_info=True)

        # We either have a differing status code, add an error for this service
        # This would imply that we were not able to connect to the esec-client
        service_dict = get_service_check_dict(500, service_from, service_to,
                                              "Error: Could not connect")

    return service_dict


def get_service_check_dict(status_code, service_from, service_to, service_message, service_alembic_version=None):

    service_dict = {
        "status_code": status_code,
        "service_from": service_from,
        "service_to": service_to,
        "service_message": service_message
    }

    if service_alembic_version is not None:
        service_dict["service_alembic_version"] = service_alembic_version

    return service_dict


def get_multiple_dict_values(service_from, service_to, interface_name, service_list):

    try:
        # Append the return values to the service_list and return it
        service_response_dict = get_service_check_response(service_from, service_to, interface_name)

        if len(service_response_dict) == 2:
            # For 200 success: two services
            service_list["services"].append(service_response_dict[0])
            service_list["services"].append(service_response_dict[1])
        else:
            # If there is an error response
            service_list["services"].append(service_response_dict)

    except IndexError as e:
        serviceIndexError = get_service_check_dict(500, "deed-api", "title adapter stub/api",
                                                   "The response has triggered an index exception")
        service_list["services"].append(serviceIndexError)
        app.logger.error("Index Error at the service-check route: %s", (e,), exc_info=True)

    return service_list


@app.errorhandler(EsecException)
def esecurity_error(e):
    app.logger.error("ESecurity has raised an Exception: %s", (e,), exc_info=True)
    return "", 200


@app.errorhandler(FileNotFoundError)
def not_found_exception(e):
    app.logger.error("Not found error: %s", (e,), exc_info=True)
    return jsonify({"message": "Deed not found"}), 404


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error("Unhandled Exception: %s", (e,), exc_info=True)
    return jsonify({"message": "Unexpected error."}), 500


@app.errorhandler(DatabaseException)
def database_exception(e):
    app.logger.error("Database Exception: %s", (e,), exc_info=True)
    return jsonify({"message": "Database Error."}), 500
