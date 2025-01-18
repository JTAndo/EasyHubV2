# EasyHub Project Documentation

## Overview
EasyHub is a platform to connect elderly users (Non-Admins) with their family members (Admins). Admins manage user permissions, register users, and facilitate communication.

---

## Project Structure
```
EasyHub/
├── backend/            # Azure Functions + PostgreSQL backend
├── admin_app/          # Flutter Admin app
├── non_admin_app/      # Flutter Non-Admin app
├── docs/               # Documentation
└── README.md           # Project overview
```

---

## Backend
**Technologies**: Azure Functions, Python, PostgreSQL

### Features Implemented:
1. **Endpoints**:
   - `POST /registerUser`: Registers a new user.
   - `GET /getUsers`: Fetches all registered users.

2. **Database**:
   - Table: `users`
     ```sql
     CREATE TABLE users (
         id SERIAL PRIMARY KEY,
         name VARCHAR(100) NOT NULL,
         email VARCHAR(100) UNIQUE NOT NULL,
         role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Non-Admin')),
         permissions JSONB NOT NULL DEFAULT '{}',
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

3. **Environment Variables**:
   Configured via `.env` file:
   ```plaintext
   DB_HOST=localhost
   DB_NAME=easyhub
   DB_USER=admin
   DB_PASSWORD=admin
   ```

### Function Creation Commands:
1. Initialize Azure Functions:
   ```bash
   func init backend --worker-runtime python
   ```

2. Create the `registerUser` function:
   ```bash
   cd backend
   func new --name registerUser --template "HTTP trigger"
   ```

3. Create the `getUsers` function:
   ```bash
   func new --name getUsers --template "HTTP trigger"
   ```

### Key Improvements:
- **Parameterized Queries**: Prevents SQL injection.
- **Context Managers**: Handles database connections and cursors.
- **Error Handling**: Specific responses for duplicate emails and other issues.

---

## Frontend
**Technologies**: Flutter

### Admin App:
- **Features**:
  - Register new users.
  - View a list of registered users.
- **Status**: Basic structure created; UI implementation in progress.

### Non-Admin App:
- **Features**:
  - View assigned user details and permissions.
- **Status**: Not yet started.

---

## Testing
1. **Backend**:
   - Tested endpoints using `curl`:
     ```bash
     curl -X POST http://localhost:7071/api/registerUser \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john.doe@example.com", "role": "Admin", "permissions": {"remote_access": true}}'
     ```
   - Verified database entries via `psql`.

2. **Frontend**:
   - Placeholder screens implemented for Admin app.

---

## Next Steps
1. Finalize backend endpoints:
   - Add user update and delete functionality.
   - Enforce permissions logic.

2. Complete Admin app UI:
   - Integrate API calls for registration and user management.

3. Begin Non-Admin app development:
   - Fetch and display user-specific data.

4. Plan deployment:
   - Azure Functions and PostgreSQL for backend.
   - Flutter apps packaged for desktop and mobile.

