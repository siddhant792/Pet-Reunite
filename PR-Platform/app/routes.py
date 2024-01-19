"""
Module to register app routes
"""

from flask import Blueprint
from flask.app import Flask
from flask_cors import CORS

from app.main import ContactUsView, GetPaginatedLostPetsSearchResults, GetRegisterPetDetailsView, LastSeenLostPetView, LoginView, RegisterPetView, RegisterView, ReportFoundPetView

bp = Blueprint("blueprint", __name__, url_prefix="/pr-platform")

CORS(bp, resources={rf"/pr-platform/*": {"origins": "http://127.0.0.1:3000"}})

bp.add_url_rule(
    "/register",
    view_func=RegisterView.as_view("register"),
    methods=["POST"],
)

bp.add_url_rule(
    "/login",
    view_func=LoginView.as_view("login"),
    methods=["POST"],
)

bp.add_url_rule(
    "/contact-us",
    view_func=ContactUsView.as_view("contact_us"),
    methods=["POST"],
)

bp.add_url_rule(
    "/get-register-pet-details",
    view_func=GetRegisterPetDetailsView.as_view("get_register_pet_details"),
    methods=["GET"],
)

bp.add_url_rule(
    "/register-pet",
    view_func=RegisterPetView.as_view("register_pet"),
    methods=["POST"],
)

bp.add_url_rule(
    "/update-last-seen",
    view_func=LastSeenLostPetView.as_view("update_last_seen"),
    methods=["POST"],
)

bp.add_url_rule(
    "/report-found-pet",
    view_func=ReportFoundPetView.as_view("report_found_pet"),
    methods=["POST"],
)

bp.add_url_rule(
    "/search-lost-pets",
    view_func=GetPaginatedLostPetsSearchResults.as_view("search_lost_pets"),
    methods=["GET"],
)

def register_routes(app: Flask) -> None:
        app.register_blueprint(bp)
