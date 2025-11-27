from src.models.mysql.settings.mysql_model import db, Login
from src.models.mysql.repository.login_repository import LoginRepository
from src.main.controllers.login_controller import LoginController


def login_composer() -> LoginController:
    login_repository = LoginRepository(db, Login)
    login_controller = LoginController(
        login_repository)

    return login_controller
