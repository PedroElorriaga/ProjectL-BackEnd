# Users Module

The Users module handles user registration and user data management. Users can register as customers with their personal information.

## Structure

```
src/modules/users/
├── composers/
│   └── user_composer.py
├── controllers/
│   └── user_controller.py
├── dtos/
│   └── user_dto.py
├── models/
│   └── user.py
├── repositories/
│   └── user_repository.py
└── routes/
    └── user.py
```

## Model

### User (tb_usuario)

| Column            | Type         | Constraints           | Description                      |
|-------------------|--------------|-----------------------|----------------------------------|
| id                | Integer      | Primary Key           | Unique identifier                |
| hash_senha        | String(128)  | Not Null              | Bcrypt hashed password           |
| email             | String(128)  | Not Null, Unique      | User email address               |
| tipo_usuario      | Enum         | Not Null, Default: 'customer' | User role (customer/admin) |
| nome              | String(128)  | Not Null              | Full name                        |
| sexo              | Enum         | Nullable              | Gender (M/F)                     |
| cpf               | String(11)   | Not Null, Unique      | Brazilian ID (CPF)               |
| numero_tel        | String(15)   | Nullable              | Phone number                     |
| cep               | String(10)   | Nullable              | Postal code                      |
| rua               | String(128)  | Nullable              | Street address                   |
| numero_residencia | Integer      | Nullable              | House/apartment number           |
| cidade            | String(128)  | Nullable              | City                             |
| uf                | String(2)    | Nullable              | State code (e.g., SP, RJ)        |

### User Types
- `customer` - Regular customer (default)
- `admin` - Administrator with elevated permissions

## DTOs

### UserCreateRequestDTO
Request body for user registration:
```python
{
    "senha": str,              # Required - Password
    "email": EmailStr,         # Required - Valid email
    "nome": str,               # Required - Full name
    "cpf": str,                # Required - Valid CPF (11 digits)
    "sexo": str,               # Optional - M or F
    "numero_tel": str,         # Optional - Phone number
    "cep": str,                # Optional - Postal code
    "rua": str,                # Optional - Street address
    "numero_residencia": int,  # Optional - House number
    "cidade": str,             # Optional - City
    "uf": str                  # Optional - State code
}
```

### UserResponseDTO
Response format:
```python
{
    "message": str,
    "sucess": bool
}
```

## API Endpoints

Base path: `/usuario`

### POST /usuario/criar
Register a new user account.

**Authentication:** Not required

**Request Body (JSON):**
```json
{
    "senha": "securepassword123",
    "email": "user@example.com",
    "nome": "João Silva",
    "cpf": "12345678901",
    "sexo": "M",
    "numero_tel": "11999998888",
    "cep": "01310100",
    "rua": "Avenida Paulista",
    "numero_residencia": 1000,
    "cidade": "São Paulo",
    "uf": "SP"
}
```

**Success Response (201):**
```json
{
    "sucess": true,
    "message": "Usuário criado com sucesso"
}
```

**Error Responses:**

- `400` - Invalid email format
  ```json
  {
      "sucess": false,
      "message": "Email inválido"
  }
  ```

- `401` - Invalid CPF
  ```json
  {
      "sucess": false,
      "message": "Cpf inválido"
  }
  ```

- `401` - Email already in use
  ```json
  {
      "sucess": false,
      "message": "O email já esta sendo utilizado"
  }
  ```

- `401` - CPF already in use
  ```json
  {
      "sucess": false,
      "message": "O cpf já esta sendo utilizado"
  }
  ```

- `500` - Internal server error

## Validation

### CPF Validation
The module uses the `validate_docbr` library to validate Brazilian CPF numbers. Invalid CPFs are rejected with a `401` response.

### Email Validation
Email addresses are validated using Pydantic's `EmailStr` type, ensuring proper email format.

### Unique Constraints
- **Email:** Must be unique across all users
- **CPF:** Must be unique across all users

## Security Features

### Password Storage
- Passwords are hashed using bcrypt before storage
- Plain text passwords are never stored
- Hash comparison is used during login (via Login module)

### New User Defaults
- `tipo_usuario` is set to `customer` by default
- New users cannot self-assign admin privileges

## Integration with Other Modules

### Login Module
The Login module uses `UserRepository` to:
- Find users by email or ID
- Retrieve hashed passwords for verification

### Token-Protected Endpoints
User information from JWT tokens is used across modules:
- User ID for resource ownership
- User role for authorization checks
