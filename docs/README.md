# ProjectL Documentation

This documentation covers the main modules of the ProjectL API.

## Modules

| Module | Description | Documentation |
|--------|-------------|---------------|
| **Catalog** | Perfume catalog management (CRUD operations) | [CATALOG_MODULE.md](CATALOG_MODULE.md) |
| **Login** | User authentication and JWT token generation | [LOGIN_MODULE.md](LOGIN_MODULE.md) |
| **Suppliers** | Supplier/vendor management (admin only) | [SUPPLIERS_MODULE.md](SUPPLIERS_MODULE.md) |
| **Users** | User registration and management | [USERS_MODULE.md](USERS_MODULE.md) |

## Development Setup

See [DEV_DATABASE.md](DEV_DATABASE.md) for database setup instructions.

For information about the baseline migration used in CI testing, see [BASELINE_MIGRATION.md](BASELINE_MIGRATION.md).

## API Overview

### Public Endpoints
- `GET /catalogo/` - List all perfumes
- `GET /catalogo/{id}` - Get specific perfume
- `POST /login/` - Authenticate user
- `POST /usuario/criar` - Register new user

### Protected Endpoints (Requires Authentication)
- `POST /catalogo/` - Add perfume (admin)
- `PUT /catalogo/atualizar-perfume/{id}` - Update perfume (admin)
- `DELETE /catalogo/deletar-perfume/{id}` - Delete perfume (admin)
- `GET /fornecedor/` - List suppliers (admin)
- `POST /fornecedor/criar` - Create supplier (admin)
- `PUT /fornecedor/{id}/atualizar` - Update supplier (admin)
- `DELETE /fornecedor/{id}/deletar` - Delete supplier (admin)

## Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

Obtain a token via the `/login/` endpoint.

## Architecture

Each module follows a consistent structure:

```
module/
├── composers/     # Dependency injection / factory functions
├── controllers/   # Business logic
├── dtos/          # Data Transfer Objects (Pydantic models)
├── models/        # SQLAlchemy database models
├── repositories/  # Database access layer
└── routes/        # Flask Blueprint routes
```

## Technologies

- **Framework:** Flask
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Migrations:** Alembic
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt
- **Validation:** Pydantic
- **Image Upload:** Cloudinary
