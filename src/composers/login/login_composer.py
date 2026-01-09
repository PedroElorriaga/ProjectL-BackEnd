from src.databases.postgres.model.user import db, User
from src.databases.postgres.repository.user_repository import UserRepository
from src.main.controllers.login_controller import LoginController


def login_composer() -> LoginController:
    user_repository = UserRepository(db, User)
    login_controller = LoginController(
        user_repository)

    return login_controller
