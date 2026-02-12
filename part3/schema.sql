CREATE TABLE users (
	first_name VARCHAR(50) NOT NULL, 
	last_name VARCHAR(50) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(128) NOT NULL, 
	is_admin BOOLEAN, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
CREATE TABLE amenities (
	name VARCHAR(255) NOT NULL, 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE places (
	title VARCHAR(255) NOT NULL, 
	description TEXT, 
	price FLOAT, 
	latitude FLOAT, 
	longitude FLOAT, 
	owner_id VARCHAR(36), 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);
CREATE TABLE place_amenity (
	place_id VARCHAR(36) NOT NULL, 
	amenity_id VARCHAR(36) NOT NULL, 
	PRIMARY KEY (place_id, amenity_id), 
	FOREIGN KEY(place_id) REFERENCES places (id), 
	FOREIGN KEY(amenity_id) REFERENCES amenities (id)
);
CREATE TABLE reviews (
	text TEXT NOT NULL, 
	rating INTEGER NOT NULL, 
	user_id VARCHAR(36), 
	place_id VARCHAR(36), 
	id VARCHAR(36) NOT NULL, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(place_id) REFERENCES places (id)
);
