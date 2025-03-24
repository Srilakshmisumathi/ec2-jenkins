from flask import Flask, render_template, request
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database Configuration (PostgreSQL)
DB_HOST = "database-2.cn46ece8sslh.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgresql1234"

# Connect to PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    if not (name and email):
        return "Name and email are required!", 400

    # Save data to database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, created_at) VALUES (%s, %s, %s)",
            (name, email, datetime.utcnow())
        )
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return f"Error saving to database: {str(e)}", 500

    return render_template('success.html', name=name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
