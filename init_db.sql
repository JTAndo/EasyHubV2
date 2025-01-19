\connect postgres;
DROP DATABASE IF EXISTS easyhubv2;
-- Create the database
CREATE DATABASE easyhubv2;

-- Connect to the database (skip if already using the database)
\connect easyhubv2;

-- Create the admins table
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

-- Create the non_admins table
CREATE TABLE non_admins (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    family_member_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the admin_non_admin linking table
CREATE TABLE admin_non_admin (
    id SERIAL PRIMARY KEY,
    admin_id INT REFERENCES admins(id) ON DELETE CASCADE,
    non_admin_id INT REFERENCES non_admins(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (admin_id, non_admin_id)
);
