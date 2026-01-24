-- Initial data for HBnB Part 3
-- Seed data with admin user and initial amenities

-- Insert administrator user
-- Password: admin1234 (bcrypt hashed)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES
(
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$yFtOKFUJWMUvSNq8fOsebOgBjHWpBtSZl83dqkAyNQ0sFtyR8XKC.',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert initial amenities
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('a1b2c3d4-1111-2222-3333-444455556666', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('b2c3d4e5-2222-3333-4444-555566667777', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('c3d4e5f6-3333-4444-5555-666677778888', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
