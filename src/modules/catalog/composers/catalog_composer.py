from src.modules.catalog.controllers.catalog_controller import CatalogController
from src.modules.catalog.repositories.catalog_repository import CatalogRepository
from src.modules.catalog.models.catalog import db, Catalog


def catalog_composer() -> CatalogController:
    catalog_repository = CatalogRepository(db, Catalog)
    catalog_controller = CatalogController(catalog_repository)

    return catalog_controller
