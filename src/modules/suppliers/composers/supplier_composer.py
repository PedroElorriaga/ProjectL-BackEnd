from src.modules.suppliers.models.supplier import db, Supplier
from src.modules.suppliers.repositories.supplier_repository import SupplierRepository
from src.modules.suppliers.controllers.supplier_controller import SuplierController


def supplier_composer() -> SuplierController:
    supplier_repository = SupplierRepository(db, Supplier)
    supplier_controller = SuplierController(supplier_repository)

    return supplier_controller
