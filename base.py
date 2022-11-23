import sqlite3

db = sqlite3.connect('database.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
	user_id INT PRIMARY KEY,
	admin INT,
	user INT,
	ban INT,
	exit_bot INT,
	name TEXT,
	ids INT
)""")