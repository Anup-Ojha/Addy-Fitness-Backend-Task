# Backend Intern Assessment – User Management API (FastAPI + JWT)

A clean, minimal FastAPI application that provides:

- ✅ User CRUD with SQLite (SQLAlchemy ORM)  
- ✅ Pagination (skip/limit)  
- ✅ Soft delete (`is_active = False`)  
- ✅ JWT authentication (24-hour token) with bcrypt password hashing  
- ✅ Protected routes (Bearer token)  
- ✅ Clear README and examples

---

## Tech Stack

- **FastAPI** – API framework  
- **SQLAlchemy** – ORM (SQLite database)  
- **Pydantic** – request/response validation  
- **passlib[bcrypt]** – secure password hashing  
- **python-jose[cryptography]** – JWT creation/verification  
- **Uvicorn** – ASGI server

---

## Project Structure

```
task_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py          # SECRET_KEY config + JWT + bcrypt (combined)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py              # /auth/register, /auth/login
│       └── users.py             # /users/* (protected)
├── requirements.txt
└── README.md
```

> Tables are auto-created on app start via `Base.metadata.create_all(bind=engine)` in `app/main.py`.

---

## Requirements

`requirements.txt`
```
fastapi
uvicorn
sqlalchemy
pydantic
passlib[bcrypt]
python-jose[cryptography]
python-multipart
python-dotenv
```

Python 3.10+ recommended.

---

## Setup Instructions

1) **Clone the repo**
```bash
git clone https://github.com/<your-username>/backend-intern-assessment-<your-name>.git
cd backend-intern-assessment-<your-name>
```

2) **Create a virtual environment**
```bash
python -m venv venv
```

3) **Activate it**
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- Windows:
  ```bash
  venv\Scriptsctivate
  ```

4) **Install dependencies**
```bash
pip install -r requirements.txt
```

5) **Create a `.env` file** in project root (used by `app/core/security.py`)
```
SECRET_KEY=replace_with_a_secure_random_string  
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Note:- I have added my .env file in this as for only your usage which is not my personal or private security key its just a generated one**
**Note:- The venv folder is also been uploaded to git just for direct zip download and usage**
**Also it is not a best practice to do the above two things its just for a assesment is have also done as its a bad practice to do it**

> Generate a secure key:
> ```python
> import secrets; print(secrets.token_hex(32))
> ```

6) **Run the app**
```bash
uvicorn app.main:app --reload
```

7) **Open API Docs**
- Swagger UI: http://127.0.0.1:8000/docs  
- ReDoc:      http://127.0.0.1:8000/redoc

> The SQLite DB file is `sql_app.db` in the project root.

---

## Data Model

**User**
- `id` (int, PK, auto-increment)
- `email` (str, unique, required)
- `full_name` (str, optional)
- `phone` (str, optional)
- `created_at` (datetime, auto)
- `is_active` (bool, default `True`)
- `password` (str, **hashed**, never plaintext)

---

## Authentication Flow (JWT, 24h)

1. **Register** with email + password → password is **bcrypt-hashed** and stored.  
2. **Login** with email + password → returns a **JWT** with 24-hour expiry.  
3. **Use JWT** in `Authorization: Bearer <token>` header to access protected endpoints.  
4. Expired/invalid tokens → **401 Unauthorized**.

---

## Endpoints

### Auth (public)

- **POST** `/auth/register`  
  Body:
  ```json
  {
    "email": "john@example.com",
    "password": "supersecret123",
    "full_name": "John Doe",
    "phone": "9999999999"
  }
  ```
  Response:
  ```json
  {
    "access_token": "<JWT>",
    "token_type": "bearer"
  }
  ```

- **POST** `/auth/login`  
  Body:
  ```json
  {
    "email": "john@example.com",
    "password": "supersecret123"
  }
  ```
  Response:
  ```json
  {
    "access_token": "<JWT>",
    "token_type": "bearer"
  }
  ```

### Users (protected – require Bearer token)


- **POST** `/users/` → create a user (admin-like behavior) '''**Note:- This was removed as we have added the register function** '''
- **GET** `/users/{user_id}` → get user by id
- **PUT** `/users/{user_id}` → update user (name/phone/email with collision checks)
- **DELETE** `/users/{user_id}` → soft delete (`is_active = False`)

> All `/users/*` routes are protected by a dependency like `Depends(verify_token)`.

---

## Test via FastAPI Docs (Step-by-Step)

1. Open **Swagger UI** at `http://127.0.0.1:8000/docs`.
2. Expand **`POST /auth/register`**, click **Try it out**, fill the body, and **Execute**.  
   Copy the `access_token` from the response.
3. Alternatively, use **`POST /auth/login`** to get a token for an existing user.
4. Now call any **/users/** endpoints (they will succeed only with a valid token):
   - `GET /users/me` to confirm who you are.
   - `POST /users/` to create other users.
   - `GET /users/?skip=0&limit=10` to list users with pagination.
   - `PUT /users/{id}` to update, `DELETE /users/{id}` to deactivate.

---

---

## VS Code REST Client (optional)

Create `tests.http` in the repo and paste:

```http
### Register
POST http://127.0.0.1:8000/auth/register
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "supersecret123",
  "full_name": "John Doe",
  "phone": "9999999999"
}

### Login
POST http://127.0.0.1:8000/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "supersecret123"
}

### Me (paste token below)
@token = Bearer YOUR_TOKEN_HERE

GET http://127.0.0.1:8000/users/me
Authorization: {{token}}

### List Users
GET http://127.0.0.1:8000/users?skip=0&limit=10
Authorization: {{token}}

### Create User
POST http://127.0.0.1:8000/users/
Authorization: {{token}}
Content-Type: application/json

{
  "email": "alice@example.com",
  "full_name": "Alice",
  "phone": "1234567890"
}
```

Install the VS Code **REST Client** extension and click **Send Request** above each block.

---

## Common Issues & Fixes

- **`sqlite3.OperationalError: no such table: users`**  
  Make sure `Base.metadata.create_all(bind=engine)` runs before queries.  
  Restart the server if you changed models. Delete `sql_app.db` to reset.

- **Import path issues in VS Code**  
  Run with module path:  
  ```bash
  uvicorn app.main:app --reload
  ```
  Ensure `__init__.py` files exist in `app/`, `models/`, `routes/`, `schemas/`, `core/`.

---

## How This Meets the Assessment

- **Task 1**  
  - Model: `id, email, full_name, phone, created_at, is_active` ✅  
  - Endpoints: POST/GET(id)/GET(list)/PUT/DELETE ✅  
  - Pagination: `skip` + `limit` ✅  
  - Validation & errors via Pydantic + HTTPException ✅

- **Task 2**  
  - `password` (hashed, never plaintext) ✅  
  - `/auth/register`, `/auth/login` ✅  
  - JWT with 24h expiry ✅  
  - Protected routes require Bearer token ✅  
  - 401 and 422 handled ✅

---

## Run Checklist Before Submission

- [ ] `uvicorn app.main:app --reload` runs without errors  
- [ ] `/docs` opens and all endpoints work  
- [ ] Register → Login → copy token → Authorize → use `/users/*`  
- [ ] README and requirements.txt present and accurate  
- [ ] Repo is public on GitHub and link is shareable

---

## License

For assessment/educational use.
