# Notification Service

A FastAPI-based notification service with PostgreSQL backend.

## Features

- Create and retrieve notifications
- PostgreSQL database for persistence
- Docker and Docker Compose setup
- PgAdmin for database management

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd notification-service
```

2. Start the services using Docker Compose:
```bash
docker-compose up --build
```

The following services will be available:
- FastAPI Application: http://localhost:8001
- PgAdmin: http://localhost:5050
- PostgreSQL: localhost:5432

## API Endpoints

### Create Notification
```http
POST /notifications

{
    "uid": "user123",
    "body": "Notification message"
}
```

### Get User Notifications
```http
GET /users/{uid}/notifications
```

## Database Configuration

Default PostgreSQL credentials:
- Username: postgres
- Password: postgres
- Database: notifications_db

PgAdmin credentials:
- Email: admin@admin.com
- Password: admin

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

2. Install dependencies:
```bash
pip install -r app/requirements.txt
```

3. Run the application locally:
```bash
cd app
uvicorn main:app --reload --port 8001
```

## API Documentation

Once the service is running, you can access:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Project Structure
```
notification-service/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── db/
│   │   └── ops.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml
```