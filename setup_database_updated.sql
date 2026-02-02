-- Create database (optional - uncomment if needed)
-- CREATE DATABASE IF NOT EXISTS your_database;
-- USE your_database;

-- Drop table if exists (be careful with this in production!)
DROP TABLE IF EXISTS users;

-- Create users table with new fields
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mobile_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    reason_for_appointment TEXT NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO users (name, email, mobile_number, gender, reason_for_appointment, entry_time, exit_time) VALUES
    ('John Doe', 'john.doe@example.com', '+91-9876543210', 'Male', 'Business Meeting', '2024-01-29 09:00:00', '2024-01-29 11:30:00'),
    ('Jane Smith', 'jane.smith@example.com', '+91-9876543211', 'Female', 'Property Inspection', '2024-01-29 10:00:00', '2024-01-29 12:00:00'),
    ('Bob Johnson', 'bob.johnson@example.com', '+91-9876543212', 'Male', 'Maintenance Check', '2024-01-29 11:00:00', '2024-01-29 13:00:00'),
    ('Alice Williams', 'alice.williams@example.com', '+91-9876543213', 'Female', 'New Tenant Visit', '2024-01-29 14:00:00', '2024-01-29 15:30:00'),
    ('Charlie Brown', 'charlie.brown@example.com', '+91-9876543214', 'Male', 'Delivery', '2024-01-29 15:00:00', '2024-01-29 15:15:00');

-- Create indexes for faster lookups
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_mobile ON users(mobile_number);
CREATE INDEX idx_entry_time ON users(entry_time);
CREATE INDEX idx_gender ON users(gender);

-- Display the created table structure
DESCRIBE users;

-- Display the inserted data
SELECT * FROM users;
