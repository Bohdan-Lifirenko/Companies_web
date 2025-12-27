from flask import Blueprint, jsonify

class CompanyController:
    def __init__(self, service):
        self.service = service

    def blueprint(self) -> Blueprint:
        bp = Blueprint("companies", __name__)

        @bp.route("/companies/<company_id>/revenue")
        def revenue(company_id):
            return jsonify(self.service.get_revenue_history(company_id))

        @bp.route("/companies/<tax_id>", methods=["GET"])
        def get_company(tax_id: str):
            company = self.service.get_company(tax_id)
            return jsonify(company)

        return bp
