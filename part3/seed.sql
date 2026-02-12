INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES
('80303a31-cf2b-4f67-8720-e6fca460906c', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$PGRzSkp0dIWlZAfZ9URhJuTuB1bC4kK4NikQk7GFEiyBr/3vluiqK', 1, '2026-02-11 16:10:30.032668', '2026-02-11 16:10:30.032676'),
('040cefc0-b72f-4f77-b669-90e7bd6f2266', 'John', 'Doe', 'john@example.com', '$2b$12$1ZpqSv8wZhA8TM4yp14wqOu4gDFkQHGiJeGuoncwDxwtZI4jC7bk2', 0, '2026-02-11 16:10:30.272879', '2026-02-14 19:35:48'),
('68c54daa-15e7-4a84-af68-f8da93847606', 'Tariq', 'Almutairi', 'Tariq@ib.com.sa', '$2b$12$pBIh9Rt3/SLI.DWzUugvOOnSq1dMp1TNPtNn.0LIrWEW7jG2y/L6q', 0, '2026-02-14 19:39:24.724325', '2026-02-14 19:39:24.724331'),
('36f28c19-c731-4190-91fc-e01a4063f0c8', 'Shaden', 'Almansour', 'Shaden@ib.com.sa', '$2b$12$BKBTwCDIZp16NNfYaTAmvOGU8z66c7HNYrNhjI9dGpqiSzjLoGUvW', 0, '2026-02-14 19:39:41.328310', '2026-02-14 19:39:41.328316'),
('db89b1a8-0def-4f4c-929a-16f3c5a86862', 'Norah', 'Alsakran', 'Norah@ib.com', '$2b$12$tgu7XV.0sgbI6dIJGuJQyuuQACLh5.mzbZHl5XU3gSId2V8ZWRJvO', 0, '2026-02-14 19:40:09.190232', '2026-02-14 19:40:09.190237');
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('40926b37-99ea-4067-aa08-a3af55b511b0', 'WiFi', '2026-02-11 16:10:30.275801', '2026-02-11 16:10:30.275804'),
('87f22ccf-0694-4c7a-a7f1-f3bdabd67e17', 'Swimming Pool', '2026-02-11 16:10:30.276391', '2026-02-11 16:10:30.276393'),
('80a54b06-8755-4d2c-8d02-249723149001', 'Air Conditioning', '2026-02-11 16:10:30.276638', '2026-02-11 16:10:30.276639'),
('b2a66d25-a325-40c1-ab76-9beed7a68acd', 'Self access', '2026-02-14 19:40:34.215047', '2026-02-14 19:40:34.215052');
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) VALUES
('afb16d00-8c76-4b54-baaf-cde127123e2f', 'Cozy Beach House', 'A lovely beachfront property with stunning ocean views. Perfect for a relaxing vacation with family or friends.', 150.0, 25.7617, -80.1918, '80303a31-cf2b-4f67-8720-e6fca460906c', '2026-02-11 16:10:30.280080', '2026-02-11 16:10:30.280082'),
('6407cf10-1b18-4a71-95af-084ea610293f', 'Modern City Apartment', 'Stylish apartment in the heart of downtown. Walking distance to restaurants, shops, and nightlife.', 95.0, 40.7128, -74.006, '80303a31-cf2b-4f67-8720-e6fca460906c', '2026-02-11 16:10:30.280086', '2026-02-11 16:10:30.280087'),
('743be1bf-f570-4c5d-a3b2-5421170e556a', 'Mountain Retreat Cabin', 'Rustic cabin nestled in the mountains. Enjoy hiking, skiing, and beautiful nature all around.', 200.0, 39.5501, -105.7821, '80303a31-cf2b-4f67-8720-e6fca460906c', '2026-02-11 16:10:30.280090', '2026-02-11 16:10:30.280091'),
('d36f154a-304d-4cbb-a494-665bf5f5d31b', 'Luxury Penthouse Suite', 'Top-floor penthouse with panoramic city views. Premium amenities and 24/7 concierge service.', 450.0, 34.0522, -118.2437, '80303a31-cf2b-4f67-8720-e6fca460906c', '2026-02-11 16:10:30.280094', '2026-02-11 16:10:30.280094');
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('afb16d00-8c76-4b54-baaf-cde127123e2f', '87f22ccf-0694-4c7a-a7f1-f3bdabd67e17'),
('afb16d00-8c76-4b54-baaf-cde127123e2f', '40926b37-99ea-4067-aa08-a3af55b511b0'),
('afb16d00-8c76-4b54-baaf-cde127123e2f', '80a54b06-8755-4d2c-8d02-249723149001'),
('6407cf10-1b18-4a71-95af-084ea610293f', '40926b37-99ea-4067-aa08-a3af55b511b0'),
('6407cf10-1b18-4a71-95af-084ea610293f', '80a54b06-8755-4d2c-8d02-249723149001'),
('743be1bf-f570-4c5d-a3b2-5421170e556a', '40926b37-99ea-4067-aa08-a3af55b511b0'),
('d36f154a-304d-4cbb-a494-665bf5f5d31b', '87f22ccf-0694-4c7a-a7f1-f3bdabd67e17'),
('d36f154a-304d-4cbb-a494-665bf5f5d31b', '40926b37-99ea-4067-aa08-a3af55b511b0'),
('d36f154a-304d-4cbb-a494-665bf5f5d31b', '80a54b06-8755-4d2c-8d02-249723149001');
INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) VALUES
('d5b85375-799a-4ffa-ad28-6657c034bbb0', 'Amazing place! Had a wonderful stay. The beach view was incredible and the house was spotless.', 5, '040cefc0-b72f-4f77-b669-90e7bd6f2266', 'afb16d00-8c76-4b54-baaf-cde127123e2f', '2026-02-11 16:10:30.287689', '2026-02-11 16:10:30.287692'),
('c881770f-50df-4afd-a0f7-23666f0ce311', 'Great apartment! Very clean and well-located.', 4, '040cefc0-b72f-4f77-b669-90e7bd6f2266', '6407cf10-1b18-4a71-95af-084ea610293f', '2026-02-11 16:11:21.441424', '2026-02-11 16:11:21.441426'),
('ec8a8cac-05c1-4692-9ae9-78b7b1c5d086', 'its amazing ', 5, '040cefc0-b72f-4f77-b669-90e7bd6f2266', '743be1bf-f570-4c5d-a3b2-5421170e556a', '2026-02-11 16:18:16.780330', '2026-02-11 16:18:16.780336'),
('5c6fd911-3915-4d62-8fbc-2fd072d21519', 'LOVELY PLACE', 5, '040cefc0-b72f-4f77-b669-90e7bd6f2266', 'd36f154a-304d-4cbb-a494-665bf5f5d31b', '2026-02-14 19:37:20.043659', '2026-02-14 19:37:20.043664');
