# Phase I - In-Memory CLI Todo Application

A Python-based CLI todo application with full CRUD functionality (Create, Read, Update, Delete, Complete/Incomplete) for task management. Tasks are stored in-memory only with no persistence between sessions.

## Features

- **Add Task**: Create tasks with title and description
- **View Tasks**: Display all tasks with ID, title, description, and status
- **Update Task**: Modify task title and description
- **Delete Task**: Remove tasks with confirmation
- **Mark Complete/Incomplete**: Toggle task completion status
- **Exit**: Safely exit the application

## Prerequisites

- Python 3.13 or higher
- UV package manager

### Installing UV

Visit [UV documentation](https://github.com/astral-sh/uv) for installation instructions.

## Installation

1. Clone the repository
2. Navigate to project directory: `cd todo-app`
3. Install development dependencies (optional): `uv add --dev pytest`

## Running the Application

### Method 1: Run as Module (Recommended)

```bash
python -m todo_app
```

### Method 2: Run with UV

```bash
uv run python -m todo_app
```

## Usage

After launching, you'll see the main menu with 6 options: Add Task, View Tasks, Update Task, Delete Task, Mark Complete/Incomplete, Exit.

**Note**: All tasks are lost when you exit (in-memory only, no persistence).

## Project Structure

```
todo-app/
├── src/todo_app/
│   ├── models/task.py          # Task entity
│   ├── services/task_manager.py  # Business logic
│   └── cli/main.py             # CLI interface
├── pyproject.toml
└── README.md
```

## Architecture

Domain-driven design with three layers:
- **Domain**: Task entity (models/)
- **Business Logic**: TaskManager (services/)
- **Presentation**: CLI interface (cli/)

## Performance

- Application startup: < 5 seconds
- Viewing tasks: < 1 second (up to 100 tasks)
- All operations: < 2 seconds
