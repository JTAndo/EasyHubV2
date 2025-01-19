
### Features Implemented:
1. **Endpoints**:
   - `POST /registerUser`: Registers a new user (Admin or Non-Admin).
   - `GET /getUsers`: Fetches all registered users.

2. **Database**:
   - Table: `admins`
     ```sql
     CREATE TABLE admins (
         id SERIAL PRIMARY KEY,
         name VARCHAR(100) NOT NULL,
         email VARCHAR(100) UNIQUE NOT NULL,
         remote_access BOOLEAN DEFAULT FALSE,
         video_call BOOLEAN DEFAULT FALSE,
         voice_call BOOLEAN DEFAULT FALSE,
         manage_users BOOLEAN DEFAULT FALSE,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```
   - Table: `non_admins`
     ```sql
     CREATE TABLE non_admins (
         id SERIAL PRIMARY KEY,
         name VARCHAR(100) NOT NULL,
         email VARCHAR(100) UNIQUE NOT NULL,
         family_member_count INT DEFAULT 0,
         admin_ids JSONB NOT NULL DEFAULT '{}',
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         last_active TIMESTAMP
     );
     ```
   - Table: `admin_non_admin`
     ```sql
     CREATE TABLE admin_non_admin (
         id SERIAL PRIMARY KEY,
         admin_id INT REFERENCES admins(id) ON DELETE CASCADE,
         non_admin_id INT REFERENCES non_admins(id) ON DELETE CASCADE,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

3. **Environment Variables**:
   Configured via `.env` file:
   ```plaintext
   DB_HOST=localhost
   DB_NAME=easyhubv2
   DB_USER=admin
   DB_PASSWORD=admin
   ```

### Key Backend Changes:
- **New Relationship Table**: `admin_non_admin` to link Admins to Non-Admins.
- **Improved Registration**: Non-Admins can now link directly to multiple Admins.
- **Enhanced Error Handling**: Clear responses for database errors and unique constraints.
- **Modular Design**: Context managers ensure efficient database connection handling.

---

## Frontend
**Technologies**: Flutter

### Admin App:
- **Features**:
  - Register Admin and Non-Admin users.
  - Link Admins to Non-Admins during registration.
  - View a list of registered users.
- **Status**:
  - Basic structure and screens in progress.
  - API integration for registration partially implemented.

### Non-Admin App:
- **Features**:
  - View details of linked Admins and permissions.
- **Status**:
  - Development not started.

---

## Testing
1. **Backend**:
   - Tested endpoints using `curl`:
     - Register an Admin:
       ```bash
       curl -X POST http://localhost:7071/api/registerUser \
       -H "Content-Type: application/json" \
       -d '{
             "name": "Alice",
             "email": "alice@example.com",
             "role": "Admin",
             "permissions": {
               "remote_access": true,
               "video_call": true,
               "voice_call": true,
               "manage_users": true
             }
           }'
       ```
     - Register a Non-Admin:
       ```bash
       curl -X POST http://localhost:7071/api/registerUser \
       -H "Content-Type: application/json" \
       -d '{
             "name": "Mia",
             "email": "mia@example.com",
             "role": "Non-Admin",
             "linked_admins": ["alice@example.com"]
           }'
       ```
   - Verified database entries using `psql`.

2. **Frontend**:
   - Placeholder screens created for the Admin app.
   - No integration yet with backend endpoints.

---

## Current Challenges
1. **Database Relations**:
   - Linking Non-Admins to multiple Admins dynamically.

2. **Permissions Enforcement**:
   - Defining how permissions control UI features and actions.

3. **Frontend Integration**:
   - Syncing user roles and permissions between the backend and the Flutter apps.

---

## Next Steps
1. **Backend**:
   - Finalize `admin_non_admin` linking logic.
   - Add endpoints for updating and deleting users.

2. **Frontend**:
   - Complete the Admin app UI with API integration.
   - Start development of the Non-Admin app.

3. **Documentation**:
   - Maintain a detailed `docs/` directory for API reference, database schema, and deployment steps.

4. **Deployment**:
   - Host the backend on Azure Functions with PostgreSQL.
   - Build Flutter apps for desktop and mobile platforms.

---

