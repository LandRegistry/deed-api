import copy
import uuid
import os
from datetime import datetime
from builtins import FileNotFoundError
import pytz

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.operators import and_

from application import db
from application.deed.utils import process_organisation_credentials
from application.deed.deed_status import DeedStatus
from application.deed.address_utils import format_address_string

from Crypto.Hash import SHA256
import application


class Deed(db.Model):
    __tablename__ = 'deed'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    deed = db.Column(JSON)
    identity_checked = db.Column(db.String(1), nullable=False)
    status = db.Column(db.String(16), default='DRAFT')
    deed_xml = db.Column(db.LargeBinary, nullable=True)
    checksum = db.Column(db.Integer, nullable=True, default=-1)
    organisation_name = db.Column(db.String, nullable=True)
    payload_json = db.Column(JSON)
    created_date = db.Column(db.DateTime, default=datetime.utcnow(),  nullable=False)
    deed_hash = db.Column(db.String, nullable=True)

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_token():
        return str(uuid.uuid4())

    @staticmethod
    def generate_hash(deed_xml):
        return generate_hash(deed_xml)

    def get_json_doc(self):
        return copy.deepcopy(self.json_doc)

    def get_deed_status(title_number, mdref):

        deeds = Deed.query.filter(
            and_(
                Deed.deed['title_number'].astext == title_number,
                Deed.deed['md_ref'].astext == mdref
            )
        ).all()

        deeds_with_status = list(
            map(lambda deed: {
                "token": deed.token,
                "status": deed.status
            }, deeds)
        )

        return deeds_with_status

    def get_deeds_by_status(self, status):
        return Deed.query.filter(Deed.status.like(status), Deed.organisation_name != os.getenv('LR_ORGANISATION_NAME'),
                                 Deed.organisation_name.isnot(None)).count()

    def get_deed(self, deed_reference):
        conveyancer_credentials = process_organisation_credentials()
        organisation_name = conveyancer_credentials[os.getenv('DEED_CONVEYANCER_KEY')][0]

        if organisation_name != os.getenv('LR_ORGANISATION_NAME'):
            application.app.logger.debug("Internal request to view deed reference %s" % deed_reference)
            result = Deed.query.filter_by(token=str(deed_reference), organisation_name=organisation_name).first()
        else:
            result = Deed.query.filter_by(token=str(deed_reference)).first()

        return result

    def get_deed_system(self, deed_reference):
        application.app.logger.info("Internal request to get_deed_system to view deed reference %s" % deed_reference)
        result = Deed.query.filter_by(token=str(deed_reference)).first()

        return result

    @staticmethod
    def get_signed_deeds():
        conveyancer_credentials = process_organisation_credentials()
        organisation_name = conveyancer_credentials[os.getenv('DEED_CONVEYANCER_KEY')][0]

        result = Deed.query.filter_by(organisation_name=organisation_name, status=DeedStatus.all_signed.value).all()

        all_signed_deeds = list(
            map(lambda deed: deed.token, result)
        )

        return all_signed_deeds

    def get_borrower_position(self, borrower_token):
        for idx, borrower in enumerate(self.deed['borrowers'], start=1):
            if borrower_token == str(borrower['token']).upper():
                return idx
        return -1


def deed_adapter(deed_reference, use_system=False):
    """
    An adapter for the deed to enhance and return in the required form.

    :param deed_reference:
    :return: The deed with status and token attributes set
    :rtype: deed
    """
    if use_system:
        deed = Deed().get_deed_system(deed_reference)
    else:
        deed = Deed().get_deed(deed_reference)
    if deed is None:
        raise FileNotFoundError("There is no deed associated with deed id '{0}'.".format(deed_reference,))
    deed.deed['token'] = deed.token
    deed.deed['status'] = deed.status
    return deed


def deed_json_adapter(deed_reference):
    """
    An adapter for the deed to return as a dictionary for conversion to json.

    :param deed_reference:
    :return: The deed, as a dictionary.
    :rtype: dict
    """
    deed = deed_adapter(deed_reference)
    return {'deed': deed.deed}


def deed_pdf_adapter(deed_reference, use_system=False):
    """
    An adapter for the deed to return as a dictionary for conversion to json.

    :param deed_reference:
    :return: The deed, as a pdf.
    :rtype: pdf
    """
    deed_dict = deed_adapter(deed_reference, use_system=use_system).deed
    if 'effective_date' in deed_dict:
        temp = datetime.strptime(deed_dict['effective_date'], "%Y-%m-%d %H:%M:%S")
        check_time = check_time_stamp(temp)
        deed_dict["effective_date"] = check_time.strftime("%d/%m/%Y")
        deed_dict["effective_time"] = check_time.strftime("%H:%M:%S")

    property_address = (deed_dict["property_address"])
    deed_dict["property_address"] = format_address_string(property_address)
    return deed_dict


def generate_hash(deed_xml):
    hash = SHA256.new()
    hash.update(deed_xml)

    return hash.hexdigest()


def check_time_stamp(time):
    time_zone = pytz.timezone('Europe/London')
    return pytz.utc.localize(time, is_dst=None).astimezone(time_zone)
