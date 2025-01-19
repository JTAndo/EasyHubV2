# Notes for Development Workflow

## Branching Strategy
- Always create a **separate branch** for each ticket you are working on.
- Name the branch according to the ticket number. For example:
  - For ticket `FRONTEND-123`, name your branch `feature/FRONTEND-123`.
  - For ticket `BACKEND-456`, name your branch `feature/BACKEND-456`.
- Open a **Pull Request (PR)** for each completed ticket:
  - Ensure your branch is up-to-date with the main branch before opening the PR.
  - Assign at least one reviewer to the PR.
  - Clearly link the ticket in the PR description.

---

## Recent Updates (January 19, 2025)

### SuperAdmin Role
- The `admins` table now includes an `is_super_admin` column to differentiate SuperAdmins from regular Admins.
- A SuperAdmin can:
  - Add new Admins and Non-Admins.
  - Link Admins to Non-Admins.
  - Configure Admin permissions.

### Enhanced Registration Flow
- **Workflow**:
  1. A SuperAdmin (e.g., Josh) registers themselves as a SuperAdmin.
  2. The SuperAdmin adds a Non-Admin (e.g., Jane).
  3. The SuperAdmin adds an Admin (e.g., Mary) and assigns permissions excluding "Manage Other Admins."

### SQL Initialization
- Database and tables are now created automatically using the `init_db.sql` script in the Docker Compose setup.

### Improved Error Handling
- Database connection errors now provide clearer feedback.
- Unique constraint violations for emails handled gracefully.


### Features Implemented:

1. **Endpoints**:
   - `POST /registerUser`: Registers a new user (Admin or Non-Admin).
   - `GET /getUsers`: Fetches all registered users.
   - `POST /linkAdminToNonAdmin`: Links an Admin to a Non-Admin user.

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
         is_super_admin BOOLEAN DEFAULT FALSE,
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

---

## Directory Structure
The EasyHub project is divided into two main directories:

1. **`admin_app/`**:
   - The frontend codebase built using Flutter.
   - **Key Commands**:
     - Run the app: `flutter run`
     - Format code: `flutter format .`
     - Build for production: `flutter build <platform>` (e.g., `flutter build apk` for Android).

2. **`backend/`**:
   - The backend codebase using Azure Functions.
   - **Key Commands**:
     - Start the server locally: `func start`
     - Test endpoints: Use `curl` or any API client (Postman, Insomnia).

---

## Development Workflow

### Setting Up the Environment
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EasyHubV2
   ```
2. Navigate to the respective directory (`admin_app` or `backend`) based on your work focus.
3. Ensure you have the required tools installed:
   - Flutter SDK for the frontend.
   - Azure Functions Core Tools for the backend.
   - Docker for database and local environment.

### Running the Backend with Docker Compose
1. Navigate to the `backend/` directory.
2. Start the database and backend services:
   ```bash
   docker-compose up
   ```
3. Verify that the PostgreSQL database is running by connecting to it:
   ```bash
   docker exec -it easyhub_postgres psql -U admin -d easyhubv2
   ```

### SQL Initialization
- The database structure is initialized using the `init_db.sql` script located in `backend/`.
- This script:
  - Creates the `easyhubv2` database.
  - Sets up the `admins`, `non_admins`, and `admin_non_admin` tables.

---

## Testing

### Backend
- Test endpoints using `curl`:
  - Register a Super Admin:
    ```bash
    curl -X POST http://localhost:7071/api/registerUser \
    -H "Content-Type: application/json" \
    -d '{
          "name": "Josh",
          "email": "josh@example.com",
          "role": "SuperAdmin",
          "permissions": {
            "remote_access": true,
            "video_call": true,
            "voice_call": true,
            "manage_users": true
          }
        }'
    ```
  - Register an Admin:
    ```bash
    curl -X POST http://localhost:7071/api/registerUser \
    -H "Content-Type: application/json" \
    -d '{
          "name": "Mary",
          "email": "mary@example.com",
          "role": "Admin",
          "permissions": {
            "remote_access": true,
            "video_call": true,
            "voice_call": true,
            "manage_users": false
          }
        }'
    ```
  - Register a Non-Admin:
    ```bash
    curl -X POST http://localhost:7071/api/registerUser \
    -H "Content-Type: application/json" \
    -d '{
          "name": "Jane",
          "email": "jane@example.com",
          "role": "Non-Admin"
        }'
    ```
  - Link Admin to Non-Admin:
    ```bash
    curl -X POST http://localhost:7071/api/linkAdminToNonAdmin \
    -H "Content-Type: application/json" \
    -d '{
          "admin_email": "mary@example.com",
          "non_admin_email": "jane@example.com"
        }'
    ```

### Frontend
- Placeholder screens are available for basic functionality in `admin_app/`.
- Run the app locally:
  ```bash
  flutter run
  ```

---

## Current Progress
- **Super Admin**: Josh created with full permissions.
- **Admin**: Mary added with limited permissions (cannot manage other admins).
- **Non-Admin**: Jane linked to Admin Mary.

---

## Next Steps
1. **Backend**:
   - Finalize and test the `admin_non_admin` linking logic.
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

## TODOS:
1. Fix the `admins` table to include `non_admin_ids`.
2. Fix the `non_admins` table to include `admin_ids`.
3. Ensure the database migration process is seamless for future updates.
