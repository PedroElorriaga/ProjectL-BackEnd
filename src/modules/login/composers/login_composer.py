from src.modules.users.models.user import db, User
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.login.controllers.login_controller import LoginController


def login_composer() -> LoginController:
    user_repository = UserRepository(db, User)
    login_controller = LoginController(
        user_repository)

    return login_controller
