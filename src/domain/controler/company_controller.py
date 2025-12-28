from flask import Blueprint, jsonify

class CompanyController:
    def __init__(self, service):
        self.service = service

    def blueprint(self) -> Blueprint:
        bp = Blueprint("companies", __name__)

        @bp.route("/companies/<company_id>", methods=["GET"])
        def get_company(company_id: str):
            return jsonify(self.service.get_profile(company_id))

        @bp.route("/companies/<company_id>/revenue", methods=["GET"])
        def revenue(company_id:str):
            return jsonify(self.service.get_revenue_history(company_id))

        @bp.route("/companies/<company_id>/balance", methods=["GET"])
        def balance(company_id: str):
            return jsonify(self.service.get_balance_history(company_id))

        return bp
