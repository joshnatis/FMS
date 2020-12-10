/* NOTE: paths are for my Arch Linux box */

/* ==== food types table  ==== */
CREATE TABLE food_types (
    food_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(60) NOT NULL,
    calories FLOAT(2),
    health_scale INT,
    image_url VARCHAR(255)
);

LOAD DATA LOCAL INFILE '/home/josh/food_db/data/foods_with_images.csv'
INTO TABLE food_types
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


/* ==== stores table ==== */
CREATE TABLE stores (
    store_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(255),
    store_street VARCHAR(255),
    store_city VARCHAR(255),
    store_state VARCHAR(2)
);

LOAD DATA LOCAL INFILE '/home/josh/food_db/data/stores.csv'
INTO TABLE stores
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


/* ==== users table ==== */
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(20),
    user_sex VARCHAR(1)
);

LOAD DATA LOCAL INFILE '/home/josh/food_db/data/users.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


/* ==== transactions table with available col ==== */
CREATE TABLE food_instances (
    purchase_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    food_id INT NOT NULL,
    store_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT DEFAULT 1,
    total_price FLOAT(2),
    purchase_date DATE,
    expiration_date DATE,
    available BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (food_id) REFERENCES food_types (food_id),
    FOREIGN KEY (store_id) REFERENCES stores (store_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

LOAD DATA LOCAL INFILE '/home/josh/food_db/data/transactions.csv'
INTO TABLE food_instances
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
