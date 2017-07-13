import json
from flask import Blueprint, request, jsonify
from flask.ext.api import status
import application
from application.mortgage_document.model import MortgageDocument

mortgage_document_bp = Blueprint('mortgage_document', __name__,
                        template_folder='templates',
                        static_folder='static')


@mortgage_document_bp.route('/get-legal-warning/<md_ref>', methods=['GET'])
def get_legal_warning(md_ref):

    legal_warning = MortgageDocument.get_by_md(md_ref)
    return legal_warning.legal_warning


