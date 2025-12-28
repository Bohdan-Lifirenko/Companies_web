from flask import Blueprint, jsonify, request, abort


class CompanyController:
    def __init__(self, service):
        self.service = service

    def blueprint(self) -> Blueprint:
        bp = Blueprint("companies", __name__)

        @bp.route("/companies/<company_id>", methods=["GET"])
        def get_company(company_id: str):
            try:
                profile = self.service.get_profile(company_id)
                if not profile:
                    return jsonify({"error": f"Компанію з ЄДРПОУ {company_id} не знайдено"}), 404
                return jsonify(profile)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @bp.route("/companies/<company_id>/revenue", methods=["GET"])
        def revenue(company_id: str):
            try:
                revenue_data = self.service.get_revenue_history(company_id)
                if not revenue_data:
                    return jsonify({"error": f"Дані про доходи для компанії з ЄДРПОУ {company_id} не знайдено"}), 404
                return jsonify(revenue_data)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @bp.route("/companies/<company_id>/balance", methods=["GET"])
        def balance(company_id: str):
            try:
                balance_data = self.service.get_balance_history(company_id)
                if not balance_data:
                    return jsonify({"error": f"Дані балансу для компанії з ЄДРПОУ {company_id} не знайдено"}), 404
                return jsonify(balance_data)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        return bp
