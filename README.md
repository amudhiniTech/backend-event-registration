# Backend Event Registration API

A Python Flask REST API for registering students for the Celestius Backend Development Workshop.

## Event details

- **Event:** Backend Development Workshop
- **Date:** 20 October 2026
- **Capacity:** 50 participants

## Features

- Register a student.
- View all registrations.
- View one registration by ID.
- Validate required name and email fields.
- Validate email format.
- Prevent duplicate email registrations.
- Reject registrations after 50 participants.
- Store registration time automatically.
- Store data in a local SQLite database.
- Return clear JSON error responses.

## Technologies

- Python 3
- Flask
- SQLite
- REST API

## Project files

```text
main.py           Main Flask application and API routes
requirements.txt  Required Python package
.gitignore        Files excluded from GitHub
README.md         Project documentation
```

The SQLite database file `registrations.db` is created automatically when the application starts. It is intentionally not included in the repository so that every installation starts with a clean database.

## Setup on Windows PowerShell

Open PowerShell in the project folder and create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current window, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install the dependency:

```powershell
python -m pip install -r requirements.txt
```

## Run the application

```powershell
python main.py
```

The server runs at:

```text
http://127.0.0.1:5000
```

Keep the PowerShell window open while using the API.

## API endpoints

### Health check

```http
GET /
```

### Register a student

```http
POST /register
```

Example JSON body:

```json
{
  "name": "Anita Sharma",
  "email": "anita@example.com",
  "college": "ABC College",
  "department": "Computer Science"
}
```

`name` and `email` are required. `college` and `department` are optional.

Successful registrations return HTTP `201 Created`.

### View all registrations

```http
GET /registrations
```

The response includes the event capacity, number registered, remaining seats, and registration list.

### View one registration

```http
GET /registrations/{id}
```

Example:

```http
GET /registrations/1
```

## Error responses

- `400 Bad Request`: missing or invalid input.
- `404 Not Found`: registration ID does not exist.
- `409 Conflict`: duplicate email or event capacity reached.

Example duplicate response:

```json
{
  "error": "This email is already registered"
}
```

Example full-event response:

```json
{
  "error": "Event is full"
}
```

## Manual testing

1. Start the server with `python main.py`.
2. Open `http://127.0.0.1:5000` in a browser.
3. Open `http://127.0.0.1:5000/registrations` to view registrations.
4. Use Postman, PowerShell, or another API client to send a `POST /register` request.
5. Submit the same email twice to test duplicate prevention.
6. Request a non-existing ID such as `/registrations/999` to test the not-found response.

## Future improvements

For a production version, I would add automated tests, organizer authentication, pagination, structured logging, environment-based configuration, and a production database such as PostgreSQL.
