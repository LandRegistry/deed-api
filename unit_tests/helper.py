from application.deed.model import Deed
from application.borrower.model import Borrower
from .deed_dict import DEED
from .complete_deed_dict import complete_deed_dict
import requests

# flake8: noqa


class DeedModelMock(Deed):
    token = "ABC1234"
    deed = DEED
    deed_hash = "d4c220637b3338e0af749d4e1cd276d950973fa9bbff4011f61a757aa4f4f638"
    status = "DRAFT"
    deed_xml = "<dm-application xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"http://localhost:9080/schemas/deed-schema-v0-3.xsd\">\
                <operativeDeed><deedData Id=\"deedData\"><titleNumber>GR515835</titleNumber><propertyDescription>0 The Drive, This Town, This County, PL0 0TH</propertyDescription>\
                <borrowers><borrower><name><privateIndividual><forename>Paul</forename><middlename>James</middlename><surname>Smythe</surname>\
                </privateIndividual></name><address>borrower address</address></borrower><borrower><name><privateIndividual><forename>Jane</forename><surname>Smythe</surname>\
                </privateIndividual></name><address>borrower address</address></borrower></borrowers><mdRef>e-MD12344</mdRef><chargeClause><creCode>CRE001</creCode>\
                <entryText>The borrower, with full title guarantee, charges to the lender the property by way of legal mortgage with payment of all money secured by this charge.</entryText>\
                </chargeClause><additionalProvisions><provision><code>addp001</code><entryText>This Mortgage Deed incorporates the &lt;a href=\'#\' rel=\'external\'&gt;Lenders Mortgage Conditions\
                 and Explanation 2006&lt;/a&gt;, a copy of which the borrower has received.</entryText><sequenceNumber>0</sequenceNumber></provision><provision><code>addp002</code>\
                 <entryText>The lender is obliged to make further advances and applies for the obligation to be entered in the register.</entryText>\
                 <sequenceNumber>1</sequenceNumber></provision><provision><code>addp003</code><entryText>The borrower applies to enter a restriction in the register that no disposition \
                 of the registered estate by the proprietor of the registered estate is to be registered without a written consent signed by the proprietor for the time being of the \
                 charge dated [the date of this charge] in favour of Bank of Test Plc referred to in the charges register.</entryText><sequenceNumber>2</sequenceNumber>\
                 </provision></additionalProvisions><lender><organisationName><company><name>Bank of Test Plc</name></company></organisationName>\
                 <address>0 Test Place, Test Street, London NW0 0TQ</address><companyRegistrationDetails>Company registration number: 2347676</companyRegistrationDetails>\
                 </lender><effectiveClause>This charge takes effect when the registrar receives notification from Test Organisation that the charge is to take effect.</effectiveClause>\
                 <reference>A test reference</reference></deedData><signatureSlots><borrower_signature><signature/><signatory><privateIndividual><forename>Paul</forename><middlename>James</middlename><surname>Smythe</surname>\
                 </privateIndividual></signatory></borrower_signature><borrower_signature><signature/><signatory><privateIndividual><forename>Jane</forename><surname>Smythe</surname>\
                 </privateIndividual></signatory></borrower_signature></signatureSlots></operativeDeed><effectiveDate/><authSignature/></dm-application>"

class BorrowerModelMock(Borrower):
    token = "AAAA"
    deed_token = "ABC1234"
    forename = "Fred"
    middlename = "Ann"
    surname = "Bloggs"
    dob = "23/01/1985"
    gender = "Male"
    phonenumber = "666"
    address = "Test Address, The Place, PL9 8DR"
    esec_user_name = "dm-fred"
    signing_in_progress = None

class BorrowerModelMockNoId(Borrower):
    token = "AAAA"
    deed_token = "ABC1234"
    forename = "Fred"
    middlename = "Ann"
    surname = "Bloggs"
    dob = "23/01/1985"
    gender = "Male"
    phonenumber = "666"
    address = "Test Address, The Place, PL9 8DR"
    esec_user_name = None
    signing_in_progress = None


class EsecClientMock():

    def auth_sms(self, deed, borrower_pos, esec_id, borrower_code, borrower_token):
        return "", 200

class MortgageDocMock:
    md_ref = "e-MD12121"
    data = '{"description":"test setup charge clause","lender":{ "name":"a new lender",' \
           '"address":"no 1 reputable street"}, "charge_clause": { "cre_code": "CRE001",' \
           '"description":"This is an example charge clause"}, "additional_provisions": ' \
           '[ { "additional_provision_code":"addp001", "description":"this is additional ' \
           'provision1"}, { "additional_provision_code":"addp002", "description":"this is ' \
           'additional provision2"}]}'


class MortgageDocMockWithReference:
    md_ref = "e-MD1291A"
    data = '{"description":"test setup charge clause","lender":{ "name":"a new lender",' \
           '"address":"no 1 reputable street"}, "lender_reference_name":"Random Company",' \
           '"charge_clause": { "cre_code": "CRE001",' \
           '"description":"This is an example charge clause"}, "additional_provisions": ' \
           '[ { "additional_provision_code":"addp001", "description":"this is additional ' \
           'provision1"}, { "additional_provision_code":"addp002", "description":"this is ' \
           'additional provision2"}]}'


class MortgageDocMockWithDateOfMortgageOffer:
    md_ref = "e-MD1291A"
    data = '{"description":"test setup charge clause","lender":{ "name":"a new lender",' \
           '"address":"no 1 reputable street"}, "date_of_mortgage_offer_heading":"a date",' \
           '"charge_clause": { "cre_code": "CRE001",' \
           '"description":"This is an example charge clause"}, "additional_provisions": ' \
           '[ { "additional_provision_code":"addp001", "description":"this is additional ' \
           'provision1"}, { "additional_provision_code":"addp002", "description":"this is ' \
           'additional provision2"}]}'
    deed = complete_deed_dict


class MortgageDocMockWithDeedEffector:
    md_ref = "e-MD1291A"
    data = '{"description":"test setup charge clause","lender":{ "name":"a new lender",' \
           '"address":"no 1 reputable street"}, "deed_effector":"Different Name",' \
           '"charge_clause": { "cre_code": "CRE001",' \
           '"description":"This is an example charge clause"}, "additional_provisions": ' \
           '[ { "additional_provision_code":"addp001", "description":"this is additional ' \
           'provision1"}, { "additional_provision_code":"addp002", "description":"this is ' \
           'additional provision2"}]}'
    deed = complete_deed_dict


class DeedHelper:
    _json_doc = {
        "title_number": "GR515835",
        "md_ref": "e-MD12344",
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _json_doc_with_reference = {
        "title_number": "GR515835",
        "md_ref": "e-MD12344",
        "property_address": "5 The Drive, This Town, This County, PL4 4TH",
        "reference": "Test reference",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _json_doc_future_dob = {
        "title_number": "GR515835",
        "md_ref": "e-MD12344",
        "property_address": "5 The Drive, This Town, This County, PL4 4TH",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/2022",
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/2022",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _json_doc_update = {
        "title_number": "DN100",
        "md_ref": "e-MD12345",
        "property_address": "100 The Drive, This Town, This County, PL4 4TH",
        "borrowers": [
            {
                "forename": "Ann",
                "middle_name": "Luke",
                "surname": "Duck",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JX",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _valid_initial_deed = {
                "title_number": "GR515835",
                "md_ref": "e-MD12344",
                "borrowers": [],
                "charge_clause": [],
                "additional_provisions": [],
                "property_address": "0 The Drive, This Town, This County, PL0 0TH",
                "effective_clause": ""
            }

    _invalid_title = {
        "title_number": "BBBB12313212BB",
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "md_ref": "mortgageref",
        "borrowers": [
            {
                "forename": "fred",
                "middle_name": "joe",
                "surname": "bloggs"
            },
            {
                "forename": "lisa",
                "surname": "bloggette"
            }
        ],
        "identity_checked": "Y"
    }

    _borrowers_with_same_phonenumber = {
        "title_number": "BBBB12313212BB",
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "md_ref": "mortgageref",
        "borrowers": [
            {
                "forename": "fred",
                "middle_name": "joe",
                "surname": "bloggs",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            },
            {
                "forename": "lisa",
                "surname": "bloggette",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _valid_borrowers = {
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "M",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "M",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ]
    }

    _valid_borrowers_with_ids = {
        "title_number": "DN100",
        "md_ref": "e-MD12344",
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "id": 1,
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "id": 2,
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y"
    }

    _valid_single_borrower_update = {
                "id": 25,
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "M",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
                }
    _valid_single_borrower_update_response = {
                "id": "9999",
                "token": "AAAAAAAA",
                "forename": "Lisa",
                "middle_name": "Ann",
                "surname": "Bloggette"
                }

    _invalid_phone_numbers = {"borrowers": [
        {
            "forename": "lisa",
            "middle_name": "ann",
            "surname": "bloggette",
            "gender": "M",
            "address": "test address with postcode, PL0 0JR",
            "dob": "02/02/1922",
            "phone_number": "07777777776"
        },
        {
            "forename": "frank",
            "middle_name": "ann",
            "surname": "bloggette",
            "gender": "M",
            "address": "Test Address With Postcode, PL0 0JR",
            "dob": "02/02/1922",
            "phone_number": "07777777777"
        }
    ]}
    _invalid_blanks_on_required_fields = {
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "",
                "gender": "M",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776"
            },
            {
                "forename": "",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "M",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ]
    }

    _validate_borrower = {"borrower_token": "aaaaaa", "dob": "02/02/1922", "phonenumber": "07777777777"}

    _validate_borrower_dob = {"borrower_token": "aaaaaa", "dob": "02/02/1922"}

    _invalid_blank_address = {
        "title_number": "DN100",
        "md_ref": "e-MD12344",
        "property_address": "",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777"
            }
        ],
        "identity_checked": "Y",
    }

    _add_borrower_signature = {"borrower_token": "3"}

    _verify_and_sign = {"borrower_token": "3",
                        "authentication_code": "aW23xw"}

    _modify_existing_deed = {
        "title_number": "GR515835",
        "md_ref": "e-MD12344",
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "borrowers": [
            {
                "forename": "lisa",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Male",
                "address": "test address with postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777776",
                "id": "1"
            },
            {
                "forename": "frank",
                "middle_name": "ann",
                "surname": "bloggette",
                "gender": "Female",
                "address": "Test Address With Postcode, PL0 0JR",
                "dob": "02/02/1922",
                "phone_number": "07777777777",
                "id": "2"
            }
        ],
        "identity_checked": "Y"
    }

    _update_deed_mock_response = {
        "effective_clause": "",
        "additional_provisions": [],
        "property_address": "0 The Drive, This Town, This County, PL0 0TH",
        "charge_clause": [],
        "title_number": "GR515835",
        "borrowers": [{
            "surname": "Bloggette",
            "token": "AAAAAAAA",
            "middle_name": "Ann",
            "id": "9999",
            "forename": "Lisa"
        },
            {
                "surname": "Bloggette",
                "token": "AAAAAAAA",
                "middle_name": "Ann",
                "id": "9999",
                "forename": "Lisa"
            }],
        "md_ref": "e-MD12344"
    }

    _create_deed_and_update_akuma = {
        "result": "A",
        "id": "2b9115b2-d956-11e5-942f-08002719cd16"
    }


class StatusMock:
    _status_with_mdref_and_titleno = [
        {
            "status": "DRAFT",
            "token": "c91d57"
        }
    ]

    _no_status_with_mdref_and_titleno = [
    ]


class AkumaMock:
    _approved_akuma_payload = {
        "payload": {
            "title_number": "DN100",
            "md_ref": "e-MD12344",
            "property_address": "0 The Drive, This Town, This County, PL0 0TH",
            "borrowers": [
                {
                    "forename": "lisa",
                    "middle_name": "ann",
                    "surname": "bloggette",
                    "gender": "Male",
                    "address": "test address with postcode, PL0 0JR",
                    "dob": "02/02/1922",
                    "phone_number": "07777777776"
                },
                {
                    "forename": "frank",
                    "middle_name": "ann",
                    "surname": "bloggette",
                    "gender": "Female",
                    "address": "Test Address With Postcode, PL0 0JR",
                    "dob": "02/02/1922",
                    "phone_number": "07777777777"
                }
            ],
            "identity_checked": "Y",
            "title_no": "DN100",
            "organisation_locale": "gb",
            "organisation_name": "Test Organisation",
            "deed_token": "bb34300c-ba9b-4d86-b28f-ab793e0d45fa"
        },
        "service": "digital mortgage",
        "activity": "create deed"

    }


class FakeResponse(requests.Response):

    def __init__(self, content='', status_code=200):
        super(FakeResponse, self).__init__()
        self._content = content
        self._content_consumed = True
        self.status_code = status_code


def borrower_object_helper(borrower):
    new_borrower = Borrower()

    new_borrower.id = borrower['id']
    new_borrower.token = "AAAA"
    new_borrower.deed_token = "AAAA"
    new_borrower.forename = borrower['forename']
    new_borrower.middlename = borrower['middle_name']
    new_borrower.surname = borrower['surname']
    new_borrower.dob = borrower['dob']
    new_borrower.gender = borrower['gender']
    new_borrower.phonenumber = borrower['phone_number']
    new_borrower.address = borrower['address']
    new_borrower.esec_user_name = ""

    return new_borrower
