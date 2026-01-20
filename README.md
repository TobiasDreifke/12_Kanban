# Kanban Board Backend (Django REST Framework)

This is the backend for a Kanban board application, built with Django and Django REST Framework (DRF). It provides a RESTful API for managing boards, tasks, and comments with integrated user authentication and role-based permissions.

## Features
- **Authentication**: Token-based login, registration, and logout.
- **Board Management**: Create boards, manage members, and track board statistics.
- **Task System**: Create and assign tasks with status tracking (To-Do, In Progress, Done) and priorities.
- **Task Filters**: Specific endpoints for tasks assigned to the user or awaiting review.
- **Comment System**: Add and delete comments on specific tasks.
- **Permissions**: Granular access control (Owners vs. Members vs. Authors).

## Tech Stack
- Python 3.x
- Django 5.x
- Django REST Framework (DRF)
- SQLite (Default database)

## Prerequisites
Ensure you have Python and `pip` installed on your machine.

## Getting Started

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
Create a virtual environment:

Bash

python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
Apply migrations:

Bash

python manage.py migrate
Run the server:

Bash

python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

API Endpoints Overview
/auth/api/registration/ - User registration

/auth/api/login/ - Token-based login

/kanban/api/boards/ - List/Create boards

/kanban/api/tasks/ - Manage tasks

/kanban/api/tasks/<task_id>/comments/ - Task-specific comments

Development Conventions
Project Structure: Core settings are located in the core folder.

App Structure: Each app contains an api/ folder for serializers, views, and URLs.

Code Style: Following PEP8 guidelines.

License
This project is for educational purposes.


---
