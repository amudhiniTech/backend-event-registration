from datetime import datetime, timezone
import re
import sqlite3

from flask import Flask, jsonify, request


app = Flask(__name__)

DATABASE_FILE = "registrations.db"
EVENT_NAME = "Backend Development Workshop"
EVENT_DATE = "20 October 2026"
EVENT_CAPACITY = 50


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            college TEXT,
            department TEXT,
            registered_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def registration_to_dict(registration):
    return {
        "id": registration["id"],
        "name": registration["name"],
        "email": registration["email"],
        "college": registration["college"],
        "department": registration["department"],
        "registered_at": registration["registered_at"],
    }


@app.get("/")
def home():
    return jsonify(
        {
            "message": "Event Registration API is running",
            "available_endpoints": [
                "POST /register",
                "GET /registrations",
                "GET /registrations/<id>",
            ],
        }
    )


@app.post("/register")
def register_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    name = data.get("name")
    email = data.get("email")
    college = data.get("college")
    department = data.get("department")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({"error": "Email is required"}), 400

    name = name.strip()
    email = email.strip().lower()

    if not is_valid_email(email):
        return jsonify({"error": "Email format is invalid"}), 400

    connection = get_connection()

    existing_registration = connection.execute(
        "SELECT id FROM registrations WHERE email = ?",
        (email,),
    ).fetchone()

    if existing_registration:
        connection.close()
        return jsonify({"error": "This email is already registered"}), 409

    registered_count = connection.execute(
        "SELECT COUNT(*) AS count FROM registrations"
    ).fetchone()["count"]

    if registered_count >= EVENT_CAPACITY:
        connection.close()
        return jsonify({"error": "Event is full"}), 409

    registered_at = datetime.now(timezone.utc).isoformat()

    cursor = connection.execute(
        """
        INSERT INTO registrations
        (name, email, college, department, registered_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, college, department, registered_at),
    )

    connection.commit()

    new_registration = connection.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()

    connection.close()

    return jsonify(registration_to_dict(new_registration)), 201


@app.get("/registrations")
def get_registrations():
    connection = get_connection()

    registrations = connection.execute(
        "SELECT * FROM registrations ORDER BY id ASC"
    ).fetchall()

    connection.close()

    registration_list = [
        registration_to_dict(registration) for registration in registrations
    ]
    registered_count = len(registration_list)

    return jsonify(
        {
            "event": EVENT_NAME,
            "event_date": EVENT_DATE,
            "capacity": EVENT_CAPACITY,
            "registered_count": registered_count,
            "remaining_seats": EVENT_CAPACITY - registered_count,
            "registrations": registration_list,
        }
    )


@app.get("/registrations/<int:registration_id>")
def get_registration(registration_id):
    connection = get_connection()

    registration = connection.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (registration_id,),
    ).fetchone()

    connection.close()

    if registration is None:
        return jsonify({"error": "Registration not found"}), 404

    return jsonify(registration_to_dict(registration))


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
