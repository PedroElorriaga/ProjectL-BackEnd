from src.main.controllers.supplier_controller import SuplierController
from src.databases.postgres.repository.supplier_repository import SupplierRepository
from src.databases.postgres.model.supplier import db, Supplier


def supplier_composer() -> SuplierController:
    supplier_repository = SupplierRepository(db, Supplier)
    supplier_controller = SuplierController(supplier_repository)

    return supplier_controller
