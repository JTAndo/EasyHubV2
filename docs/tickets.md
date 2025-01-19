### Backend Tickets: To avoid using Jira, please update ticket with status during your push (in-progress, blocked, QA, etc)

#### **BACKEND-001**: Implement User Registration Endpoint (IN-PROGRESS)
- **Description**: Create an API endpoint for registering users as SuperAdmin, Admin, or NonAdmin.
- **Acceptance Criteria**:
  - SuperAdmins can create Admins and NonAdmins.
  - Admins cannot create other Admins.
  - Ensure permissions are correctly stored in the database.
- **Priority**: High

#### **BACKEND-002**: Implement Admin-to-NonAdmin Linking (IN-PROGRESS)
- **Description**: Create an endpoint to link Admins to NonAdmins via the `admin_non_admin` table.
- **Acceptance Criteria**:
  - Validate that both Admin and NonAdmin exist before linking.
  - Handle edge cases where Admin or NonAdmin is missing.
  - Return meaningful error messages for invalid requests.
- **Priority**: Medium

#### **BACKEND-003**: Fetch All Users API
- **Description**: Create an API endpoint to fetch all users and their roles from the database.
- **Acceptance Criteria**:
  - Endpoint should return users with their IDs, names, emails, and roles.
  - Include pagination for large datasets.
- **Priority**: Low

#### **BACKEND-004**: Add Authentication and Role-Based Access Control
- **Description**: Implement token-based authentication (JWT) and restrict access to endpoints based on roles.
- **Acceptance Criteria**:
  - Only authenticated users can access the APIs.
  - Enforce role-based permissions for API access.
- **Priority**: High

#### **BACKEND-005**: Improve Database Error Handling
- **Description**: Add comprehensive error handling for database connectivity and query issues.
- **Acceptance Criteria**:
  - Catch and log all database errors.
  - Return descriptive error messages in API responses.
- **Priority**: Medium

---

### Frontend Tickets:

#### **FRONTEND-001**: User Registration Form
- **Description**: Create a user registration form for adding SuperAdmins, Admins, and NonAdmins.
- **Acceptance Criteria**:
  - Form should include fields for name, email, role, and permissions.
  - Validate inputs before submitting.
- **Priority**: High

#### **FRONTEND-002**: Admin Dashboard
- **Description**: Design and implement a dashboard for SuperAdmins and Admins to manage users.
- **Acceptance Criteria**:
  - SuperAdmins can view all users and manage Admins.
  - Admins can view and manage linked NonAdmins.
- **Priority**: High

#### **FRONTEND-003**: User Linking Interface
- **Description**: Provide an interface to link Admins with NonAdmins.
- **Acceptance Criteria**:
  - Dropdowns for selecting Admin and NonAdmin.
  - Show successful link creation or error messages.
- **Priority**: Medium

#### **FRONTEND-004**: View All Users Page
- **Description**: Create a page to list all users with their roles and associated details.
- **Acceptance Criteria**:
  - Include pagination and search functionality.
  - SuperAdmins can see all users; Admins can see only their linked NonAdmins.
- **Priority**: Medium

#### **FRONTEND-005**: Error Display Component
- **Description**: Implement a reusable component for displaying errors across the application.
- **Acceptance Criteria**:
  - Should be customizable with error messages.
  - Support different alert levels (info, warning, error).
- **Priority**: Low
