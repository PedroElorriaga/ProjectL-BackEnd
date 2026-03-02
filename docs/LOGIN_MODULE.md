# Login Module

The Login module handles user authentication, validating credentials and generating JWT tokens for authorized access to protected resources.

## Structure

```
src/modules/login/
├── composers/
│   └── login_composer.py
├── controllers/
│   └── login_controller.py
├── dtos/
│   └── login_dto.py
└── routes/
    └── login.py
```

**Note:** This module does not have its own model or repository. It uses the `UserRepository` from the Users module to validate credentials.

## DTOs

### LoginRequestDTO
Request body for login:
```python
{
    "email": EmailStr,    # Optional (required if id not provided)
    "senha": str          # Required - password
}
```

### LoginResponseDTO
Response format:
```python
{
    "message": str,
    "sucess": bool,
    "access_token": str   # Optional - JWT token on successful login
}
```

## API Endpoints

Base path: `/login`

### POST /login/
Authenticate user with email and password.

**Authentication:** Not required

**Request Body (JSON):**
```json
{
    "email": "user@example.com",
    "senha": "userpassword"
}
```

**Success Response (200):**
```json
{
    "sucess": true,
    "message": "Login Efetuado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Error Responses:**
- `401` - Email ou senha incorretos
- `404` - Email não existe
- `500` - Internal server error

---

### POST /login/{id_credential}
Authenticate user by ID instead of email.

**Authentication:** Not required

**Path Parameters:**
- `id_credential` - User ID

**Request Body (JSON):**
```json
{
    "senha": "userpassword"
}
```

**Success Response (200):**
```json
{
    "sucess": true,
    "message": "Login Efetuado com sucesso",
    "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Error Responses:**
- `401` - Senha incorreta
- `404` - ID não existe
- `500` - Internal server error

## Authentication Flow

1. User submits email/ID and password
2. System retrieves user data from database
3. Password is verified using bcrypt hash comparison
4. On success, a JWT token is generated containing:
   - User ID
   - User type (role: `customer` or `admin`)
5. Token is returned to the client

## Using the Token

After successful login, include the JWT token in subsequent requests:

```
Authorization: Bearer <access_token>
```

Protected endpoints validate the token using the `@token_required` decorator.

## Security Features

- **Password Hashing:** Passwords are stored as bcrypt hashes
- **JWT Tokens:** Secure token-based authentication
- **Role-based Access:** Token contains user role for authorization checks
