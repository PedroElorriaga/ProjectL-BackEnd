from src.modules.users.models.user import db, User
from src.modules.users.repositories.user_repository import UserRepository
from src.modules.users.controllers.user_controller import UserController


def user_composer() -> UserController:
    user_repository = UserRepository(db, User)
    user_controller = UserController(
        user_repository)

    return user_controller
