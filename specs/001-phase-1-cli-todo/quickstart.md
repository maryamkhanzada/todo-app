# Quickstart Guide: Phase I - In-Memory CLI Todo Application

**Feature**: 001-phase-1-cli-todo
**Date**: 2025-12-27
**Version**: 1.0

## Prerequisites

Before running the Phase I Todo application, ensure you have:

1. **Python 3.13 or higher** installed
   - Verify: `python --version` or `python3 --version`
   - Should output: `Python 3.13.x` or higher

2. **UV package manager** installed
   - Install: Visit [UV documentation](https://github.com/astral-sh/uv) for installation instructions
   - Verify: `uv --version`

3. **Git** (optional, for cloning repository)
   - Verify: `git --version`

## Installation

### Option 1: Clone Repository

```bash
git clone <repository-url>
cd todo-app
```

### Option 2: Download Source

Download and extract the source code, then navigate to the project directory.

## Project Setup

### 1. Initialize UV Project

From the project root directory:

```bash
uv init
```

This initializes the UV project and creates the necessary configuration files.

### 2. Install Dependencies

**Note**: Phase I has no external runtime dependencies (Python standard library only). However, development dependencies (pytest for testing) can be installed:

```bash
uv add --dev pytest
```

### 3. Verify Python Version

Ensure the project uses Python 3.13+:

```bash
uv python install 3.13
uv python pin 3.13
```

## Running the Application

### Method 1: Run as Module (Recommended)

From the project root directory:

```bash
python -m todo_app
```

or

```bash
python3 -m todo_app
```

### Method 2: Run with UV

```bash
uv run python -m todo_app
```

## Using the Application

### Main Menu

After launching, you'll see the main menu:

```
=================================
    TODO APPLICATION - MENU
=================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

### Adding a Task

1. Enter `1` to select "Add Task"
2. Enter a title when prompted (e.g., "Buy groceries")
3. Enter a description when prompted (e.g., "Milk, eggs, bread")
4. System confirms task creation with a unique ID

**Example**:
```
Enter task title: Buy groceries
Enter task description: Milk, eggs, bread
Task added successfully! Task ID: 1
```

### Viewing Tasks

1. Enter `2` to select "View Tasks"
2. System displays all tasks with their details

**Example Output**:
```
=================================
         ALL TASKS
=================================

Task ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Status: Pending

---------------------------------
```

### Updating a Task

1. Enter `3` to select "Update Task"
2. Enter the task ID you want to update
3. Enter a new title (or press Enter to keep current)
4. Enter a new description (or press Enter to keep current)
5. System confirms the update

**Example**:
```
Enter task ID to update: 1
Current Title: Buy groceries
Enter new title (or press Enter to keep current): Buy groceries and snacks
Current Description: Milk, eggs, bread
Enter new description (or press Enter to keep current):
Task updated successfully!
```

### Deleting a Task

1. Enter `4` to select "Delete Task"
2. Enter the task ID you want to delete
3. Confirm deletion by entering "yes" or "y" (or "no"/"n" to cancel)
4. System confirms deletion or cancellation

**Example**:
```
Enter task ID to delete: 1
Are you sure you want to delete this task? (yes/no): yes
Task deleted successfully!
```

### Marking Complete/Incomplete

1. Enter `5` to select "Mark Complete/Incomplete"
2. Enter the task ID
3. System toggles the status and confirms

**Example (Pending → Completed)**:
```
Enter task ID to mark complete/incomplete: 1
Task marked as Completed!
```

**Example (Completed → Pending)**:
```
Enter task ID to mark complete/incomplete: 1
Task marked as Pending!
```

### Exiting the Application

1. Enter `6` to select "Exit"
2. Application displays goodbye message and terminates

**Note**: All tasks are lost when you exit (in-memory only, no persistence).

## Testing

### Running Unit Tests

```bash
pytest tests/unit/
```

### Running Integration Tests

```bash
pytest tests/integration/
```

### Running All Tests

```bash
pytest
```

### Test Coverage

To run tests with coverage reporting:

```bash
pytest --cov=todo_app --cov-report=term-missing
```

## Troubleshooting

### Python Version Error

**Problem**: Application requires Python 3.13+ but older version is installed

**Solution**: Install Python 3.13+ and ensure it's in your PATH, or use UV to manage Python versions:
```bash
uv python install 3.13
uv python pin 3.13
```

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'todo_app'`

**Solution**: Ensure you're running from the project root directory and the `src/` directory structure is correct.

### UV Not Installed

**Problem**: `command not found: uv`

**Solution**: Install UV following the official installation guide for your platform.

### Application Won't Start

**Problem**: Application fails to start or crashes immediately

**Solution**:
1. Verify Python version: `python --version`
2. Check project structure matches specification
3. Run with explicit Python path: `python3 -m todo_app`

## Project Structure

After setup, your project should have this structure:

```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── task_manager.py
│       └── cli/
│           ├── __init__.py
│           └── main.py
├── tests/
│   ├── unit/
│   │   ├── test_task.py
│   │   └── test_task_manager.py
│   └── integration/
│       └── test_cli.py
├── specs/
│   └── 001-phase-1-cli-todo/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── quickstart.md (this file)
│       └── contracts/
│           └── cli-interface.md
├── pyproject.toml
├── README.md
├── .python-version
└── .specify/
    └── memory/
        └── constitution.md
```

## Important Notes

### Data Persistence

⚠️ **Important**: This is Phase I with **in-memory storage only**. All tasks are lost when the application exits. This is intentional per the constitutional requirements.

### No External Dependencies

The application uses only Python standard library for runtime. External dependencies (like pytest) are development-only.

### Performance Expectations

- Application should start within 5 seconds
- Viewing tasks should be instant (< 1 second for up to 100 tasks)
- All operations should complete within 2 seconds

### Constitutional Constraints

This Phase I application strictly adheres to constitutional constraints:
- ✅ Python 3.13+
- ✅ UV package manager
- ✅ In-memory storage only
- ✅ No databases or external APIs
- ✅ CLI interface only (no GUI)
- ✅ Domain-driven architecture

## Next Steps

After successfully running the application:

1. **Explore Features**: Try all 5 core operations (Add, View, Update, Delete, Complete)
2. **Test Edge Cases**: Try invalid inputs to verify error handling
3. **Review Code**: Examine the domain-driven architecture in `src/todo_app/`
4. **Run Tests**: Execute unit and integration tests to verify functionality
5. **Review Specs**: Read specification documents in `specs/001-phase-1-cli-todo/`

## Support

For issues or questions:
- Review the feature specification: `specs/001-phase-1-cli-todo/spec.md`
- Check the implementation plan: `specs/001-phase-1-cli-todo/plan.md`
- Review the CLI interface contract: `specs/001-phase-1-cli-todo/contracts/cli-interface.md`
- Consult the project constitution: `.specify/memory/constitution.md`

## Future Phases

Phase I is the foundation. Future phases will add:
- **Phase II**: File-based persistence (tasks saved between sessions)
- **Phase III**: Database integration and advanced features
- **Phase IV**: Distributed architecture and AI integration

The simple, clean architecture of Phase I is designed to evolve gracefully into these future phases.
