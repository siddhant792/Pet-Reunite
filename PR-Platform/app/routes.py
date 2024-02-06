"""
Module to register app routes
"""

from flask import Blueprint
from flask.app import Flask

from app.main import ContactUsView, GetAnimalShelterList, GetFoundPetsSearchResults, GetLostPetsSearchResults, GetRegisterPetDetailsView, GetRegisteredPets, LastSeenLostPetView, LoginView, RegisterPetView, RegisterView, ReportFoundPetView, UpdateRegisteredPetLostStatusDetails

bp = Blueprint("blueprint", __name__, url_prefix="/pr-platform")

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
    view_func=GetLostPetsSearchResults.as_view("search_lost_pets"),
    methods=["POST"],
)

bp.add_url_rule(
    "/search-found-pets",
    view_func=GetFoundPetsSearchResults.as_view("search_found_pets"),
    methods=["POST"],
)

bp.add_url_rule(
    "/get-animal-shelters",
    view_func=GetAnimalShelterList.as_view("fetch_animal_shelters"),
    methods=["GET"],
)

bp.add_url_rule(
    "/get-user-pets/<user_id>",
    view_func=GetRegisteredPets.as_view("fetch_registered_pets"),
    methods=["GET"],
)

bp.add_url_rule(
    "/update-registered-pet-lost-status",
    view_func=UpdateRegisteredPetLostStatusDetails.as_view("update_pet_lost_status"),
    methods=["POST"],
)

def register_routes(app: Flask) -> None:
        app.register_blueprint(bp)
