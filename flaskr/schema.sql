DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS meals;

CREATE TABLE
    user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

CREATE TABLE
    meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal_idea TEXT NOT NULL,
        user_inputs TEXT NOT NULL,
        recipe_data TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )