# Catalog Module

The Catalog module manages the perfume catalog for the application. It provides CRUD operations for perfume items, with admin-only access for modifications.

## Structure

```
src/modules/catalog/
├── composers/
│   └── catalog_composer.py
├── controllers/
│   └── catalog_controller.py
├── dtos/
│   └── catalog_dto.py
├── models/
│   └── catalog.py
├── repositories/
│   └── catalog_repository.py
└── routes/
    └── catalog.py
```

## Model

### Catalog (tb_catalog)

| Column       | Type         | Constraints      | Description                        |
|--------------|--------------|------------------|------------------------------------|
| perfume_id   | Integer      | Primary Key      | Unique identifier                  |
| perfume      | String(128)  | Not Null         | Perfume name                       |
| ml           | Integer      | Not Null         | Volume in milliliters              |
| tipo         | String(128)  | Not Null         | Perfume type (e.g., EDP, EDT)      |
| preco        | Float        | Not Null         | Price                              |
| tags         | String(255)  | Not Null         | Comma-separated tags               |
| imagem_url   | String(256)  | Nullable         | URL to the perfume image           |

**Note:** Tags are stored as comma-separated strings but exposed as arrays via property getters/setters.

## DTOs

### CatalogNewPerfumeRequestDTO
Request body for creating a new perfume:
```python
{
    "perfume": str,        # Required
    "ml": int,             # Required
    "preco": float,        # Required
    "tipo": str,           # Required
    "tags": List[str],     # Required
    "imagem_url": str      # Optional
}
```

### CatalogUpdatePerfumeRequestDTO
Request body for updating a perfume (all fields optional):
```python
{
    "perfume": str,
    "ml": int,
    "preco": float,
    "tipo": str,
    "tags": List[str]
}
```

### CatalogGetPerfumeResponseDTO
Response format for perfume data:
```python
{
    "perfume_id": int,
    "perfume": str,
    "ml": int,
    "preco": float,
    "tipo": str,
    "tags": List[str],
    "imagem_url": str | None
}
```

## API Endpoints

Base path: `/catalogo`

### GET /catalogo/
Retrieve all perfumes from the catalog.

**Authentication:** Not required

**Query Parameters (optional):**
- `perfume` - Filter by perfume name (partial match)
- `tipo` - Filter by type
- `preco` - Filter by price
- `tags` - Filter by tags

**Response:**
```json
{
    "sucess": true,
    "message": [/* array of perfumes */]
}
```

---

### GET /catalogo/{id_perfume}
Retrieve a specific perfume by ID.

**Authentication:** Not required

**Response:**
```json
{
    "sucess": true,
    "message": {/* perfume object */}
}
```

**Errors:**
- `404` - Perfume not found

---

### POST /catalogo/
Add a new perfume to the catalog.

**Authentication:** Required (Admin only)

**Content-Type:** `multipart/form-data`

**Request Body:**
- `perfume` - Perfume name
- `ml` - Volume in milliliters
- `tipo` - Perfume type
- `preco` - Price
- `tags` - Comma-separated tags
- `imagem_url` - Image file (optional)

**Response:**
```json
{
    "sucess": true,
    "message": "Perfume incluido na base de dados!"
}
```

**Errors:**
- `401` - Unauthorized / Missing permissions / Item already exists
- `500` - Internal server error

---

### PUT /catalogo/atualizar-perfume/{id_perfume}
Update an existing perfume.

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
    "perfume": "string",
    "ml": 100,
    "preco": 199.99,
    "tipo": "EDP",
    "tags": ["floral", "fresh"]
}
```

**Response:**
```json
{
    "sucess": true,
    "message": "Item atualizado com sucesso!"
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Perfume not found

---

### DELETE /catalogo/deletar-perfume/{id_perfume}
Delete a perfume from the catalog.

**Authentication:** Required (Admin only)

**Response:**
```json
{
    "sucess": true,
    "message": "Item deletado com sucesso!"
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Perfume not found

## Image Upload

The module integrates with Cloudinary for image uploads. When adding a perfume with an image file, it's automatically uploaded to Cloudinary and the URL is stored.

## Authorization

- **GET endpoints:** Public access
- **POST/PUT/DELETE endpoints:** Admin role required (validated via JWT token)
