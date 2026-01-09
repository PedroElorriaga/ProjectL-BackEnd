from src.main.controllers.catalog_controller import CatalogController
from src.databases.postgres.repository.catalog_repository import CatalogRepository
from src.databases.postgres.model.catalog import db, Catalog


def catalog_composer() -> CatalogController:
    catalog_repository = CatalogRepository(db, Catalog)
    catalog_controller = CatalogController(catalog_repository)

    return catalog_controller
