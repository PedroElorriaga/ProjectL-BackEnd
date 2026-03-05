# Suppliers Module

The Suppliers module manages supplier (fornecedor) information. All operations require admin authentication.

## Structure

```
src/modules/suppliers/
├── composers/
│   └── supplier_composer.py
├── controllers/
│   └── supplier_controller.py
├── dtos/
│   └── supplier_dto.py
├── models/
│   └── supplier.py
├── repositories/
│   └── supplier_repository.py
└── routes/
    └── supplier.py
```

## Model

### Supplier (tb_fornecedor)

| Column          | Type         | Constraints      | Description                    |
|-----------------|--------------|------------------|--------------------------------|
| fornecedor_id   | Integer      | Primary Key      | Unique identifier              |
| razao_social    | String(128)  | Not Null         | Company name                   |
| email           | String(128)  | Nullable         | Contact email                  |
| cnpj            | String(14)   | Nullable         | Brazilian company ID (CNPJ)    |
| numero_tel      | String(20)   | Nullable         | Phone number                   |
| cep             | String(8)    | Nullable         | Postal code                    |
| rua             | String(128)  | Nullable         | Street address                 |
| numero_endereco | Integer      | Nullable         | Street number                  |
| cidade          | String(128)  | Nullable         | City                           |
| uf              | String(2)    | Nullable         | State code (e.g., SP, RJ)      |
| pais            | String(64)   | Nullable         | Country                        |

## DTOs

### SupplierCreateRequestDTO
Request body for creating a new supplier:
```python
{
    "razao": str,              # Required - Company name
    "email": EmailStr,         # Optional
    "cnpj": str,               # Optional
    "numero_tel": str,         # Optional
    "cep": str,                # Optional
    "rua": str,                # Optional
    "numero_endereco": int,    # Optional
    "cidade": str,             # Optional
    "uf": str,                 # Optional
    "pais": str                # Optional
}
```

### SupplierUpdateRequestDTO
Request body for updating a supplier (all fields optional):
```python
{
    "razao": str,
    "email": EmailStr,
    "cnpj": str,
    "numero_tel": str,
    "cep": str,
    "rua": str,
    "numero_endereco": int,
    "cidade": str,
    "uf": str,
    "pais": str
}
```

### SupplierGetResponseDTO
Response format for supplier data:
```python
{
    "fornecedor_id": int,
    "razao": str,
    "email": EmailStr | None,
    "cnpj": str | None,
    "numero_tel": str | None,
    "cep": str | None,
    "rua": str | None,
    "numero_endereco": int | None,
    "cidade": str | None,
    "uf": str | None,
    "pais": str | None
}
```

## API Endpoints

Base path: `/fornecedor`

### GET /fornecedor/
Retrieve all suppliers.

**Authentication:** Required (Admin only)

**Response (200):**
```json
{
    "sucess": true,
    "message": [/* array of suppliers */]
}
```

**Response (204):** No suppliers found
```json
{
    "sucess": true,
    "message": "O(s) fornecedor(s) não existe(m)"
}
```

**Errors:**
- `401` - Unauthorized

---

### GET /fornecedor/{id_supplier}
Retrieve a specific supplier by ID.

**Authentication:** Required (Admin only)

**Response (200):**
```json
{
    "sucess": true,
    "message": {/* supplier object */}
}
```

**Errors:**
- `401` - Unauthorized
- `204` - Supplier not found

---

### POST /fornecedor/criar
Create a new supplier.

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
    "razao": "Empresa LTDA",
    "email": "contato@empresa.com",
    "cnpj": "12345678000199",
    "numero_tel": "11999998888",
    "cep": "01310100",
    "rua": "Avenida Paulista",
    "numero_endereco": 1000,
    "cidade": "São Paulo",
    "uf": "SP",
    "pais": "Brasil"
}
```

**Response (201):**
```json
{
    "sucess": true,
    "message": "Fornecedor incluido com sucesso"
}
```

**Errors:**
- `401` - Unauthorized
- `500` - Internal server error

---

### PUT /fornecedor/{id_supplier}/atualizar
Update an existing supplier.

**Authentication:** Required (Admin only)

**Request Body (JSON):**
```json
{
    "razao": "Nova Razão Social",
    "email": "novo@email.com"
}
```

**Response (200):**
```json
{
    "sucess": true,
    "message": "Fornecedor atualizado com sucesso"
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Supplier not found
- `500` - Internal server error

---

### DELETE /fornecedor/{id_supplier}/deletar
Delete a supplier.

**Authentication:** Required (Admin only)

**Response (200):**
```json
{
    "sucess": true,
    "message": "Fornecedor deletado com sucesso"
}
```

**Errors:**
- `401` - Unauthorized
- `404` - Supplier not found

## Authorization

All endpoints in this module require:
1. Valid JWT token in the `Authorization` header
2. User must have `admin` role

Non-admin users will receive a `401 Unauthorized` response.
