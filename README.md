# Kanban Board Backend


This repository contains the backend for a Kanban board application, built with Python using the Django REST Framework. It provides a comprehensive RESTful API for managing users, boards, tasks, and comments with a robust permission system.

## Features

-   **User Authentication**: Secure token-based user registration, login, and logout.
-   **Board Management**: Create, view, update, and delete Kanban boards. Manage board membership by adding or removing users.
-   **Task System**: Full CRUD functionality for tasks within a board. Tasks include attributes like title, description, status (`To Do`, `In Progress`, `Done`, `Review`), priority (`Low`, `Medium`, `High`), assignee, reviewer, and due date.
-   **Commenting**: Add and delete comments on individual tasks to facilitate communication.
-   **Role-Based Permissions**: Granular access control ensures security:
    -   **Owners**: Full control over their boards, including deletion and member management.
    -   **Members**: Can view boards they are part of and create/update tasks.
    -   **Authors**: Can delete their own comments.
-   **Specialized Endpoints**: Dedicated API endpoints to retrieve tasks assigned to the current user or tasks awaiting their review.
-   **Board Statistics**: The API automatically calculates and provides key board metrics, including member count, total task count, to-do tasks, and high-priority tasks.

## Tech Stack

-   **Backend**: Python, Django, Django REST Framework
-   **Database**: SQLite3 (default)
-   **Authentication**: Django REST Framework Token Authentication
-   **CORS**: `django-cors-headers` for handling cross-origin requests.

## prerequisites

-   Python 3.x
-   `pip` (Python package installer)

## Getting Started

Follow these steps to get the project running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TobiasDreifke/12_Kanban.git
    cd 12_Kanban
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply the database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The API will now be available at `http://127.0.0.1:8000/`.

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| `POST` | `/registration/`            | Register a new user.     |
| `POST` | `/login/`                   | Log in to get a token.   |
| `POST` | `/logout/`                  | Log out and delete token.|

### Boards

| Method | Endpoint                    | Description                                  |
|--------|-----------------------------|----------------------------------------------|
| `GET`  | `/boards/`                  | List all boards the user owns or is a member of. |
| `POST` | `/boards/`                  | Create a new board.                          |
| `GET`  | `/boards/<int:pk>/`         | Retrieve details of a specific board.        |
| `PUT`  | `/boards/<int:pk>/`         | Update a board's title and member list.      |
| `DELETE`| `/boards/<int:pk>/`        | Delete a board (owner only).                 |

### Tasks

| Method | Endpoint                    | Description                                |
|--------|-----------------------------|--------------------------------------------|
| `POST` | `/tasks/`                   | Create a new task on a board.              |
| `GET`  | `/tasks/assigned-to-me/`    | Get all tasks assigned to the current user.|
| `GET`  | `/tasks/reviewing/`         | Get all tasks awaiting review by the user. |
| `GET`  | `/tasks/<int:pk>/`          | Retrieve details of a specific task.       |
| `PUT`  | `/tasks/<int:pk>/`          | Update a task's details.                   |
| `DELETE`| `/tasks/<int:pk>/`         | Delete a task.                             |

### Comments

| Method | Endpoint                                 | Description                        |
|--------|------------------------------------------|------------------------------------|
| `GET`  | `/tasks/<int:task_id>/comments/`         | List all comments for a task.      |
| `POST` | `/tasks/<int:task_id>/comments/`         | Add a new comment to a task.       |
| `DELETE`| `/tasks/<int:task_id>/comments/<int:comment_id>/` | Delete a comment (author only).    |
