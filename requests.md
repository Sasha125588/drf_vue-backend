# API Testing Guide for Postman

## Environment Setup

Create these environment variables in Postman:

- `base_url`: `http://127.0.0.1:8000`
- `access_token`: (leave empty)
- `refresh_token`: (leave empty)

## Available Endpoints

### 1. Register User

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/register/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!",
  "first_name": "Test",
  "last_name": "User"
}
```

### 2. Login

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/login/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "email": "test@example.com",
  "password": "SecurePassword123!"
}
```

### 3. Get Profile

- **Method:** GET
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`

### 4. Update Profile

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "first_name": "Updated Test",
  "last_name": "Updated User",
  "bio": "This is my updated bio"
}
```

### 5. Update Avatar

- **Method:** PATCH
- **URL:** `{{base_url}}/api/v1/auth/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body:** (form-data)
  - `avatar`: [select image file]
  - `bio`: "Updated bio with avatar"

### 6. Change Password

- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/auth/change-password/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "old_password": "SecurePassword123!",
  "new_password": "NewSecurePassword456!",
  "new_password_confirm": "NewSecurePassword456!"
}
```

### 7. Refresh Token

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/token/refresh/`
- **Headers:** `Content-Type: application/json`
- **Body:**

```json
{
  "refresh": "{{refresh_token}}"
}
```

### 8. Logout

- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/logout/`
- **Headers:**
  - `Authorization: Bearer {{access_token}}`
  - `Content-Type: application/json`
- **Body:**

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

## Common Error Responses

### Invalid Credentials (401)

```json
{
  "non_field_errors": ["Invalid credentials"]
}
```

### Missing Token (401)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Expired Token (401)

```json
{
  "detail": "Given token not valid for any token type"
}
```

### Validation Errors (400)

```json
{
  "email": ["user with this email already exists."],
  "password": ["Password fields didn't match."]
}
```

## Testing Flow

1. Register a new user
2. Login to get tokens
3. Access/update profile
4. Test other endpoints as needed
5. Logout when done
