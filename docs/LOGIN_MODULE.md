# Login Module

The Login module handles user authentication by validating credentials and generating JWT tokens for authorized access to protected resources.

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

Current validation behavior:
- `email` uses `EmailStr`
- `senha` is required
- Invalid email returns `400` with message `Email inválido`

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

**Security behavior:**
- Rate limit: `5` requests per `60` seconds per IP (`429` on exceed)
- Generic invalid credential message for wrong password: `Credenciais inválidas. Verifique seu email e senha.`

**Error Responses:**
- `400` - Invalid request payload (ex.: invalid email)
- `401` - Invalid credentials
- `404` - User ID or email not found
- `429` - Too many login attempts from same IP
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
- `401` - Credenciais inválidas
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
- **Rate Limiting:** `POST /login` protected with IP-based throttling (`5/min`)

## Tests Implemented

Current login coverage in `tests/test_api.py` includes:
- Successful login with email/password (`200`)
- Successful login using user ID (`200`)
- Wrong password returns `401`
- Invalid email format returns `400`
- Rate-limiting behavior returns `429` on 6th request within the same minute
