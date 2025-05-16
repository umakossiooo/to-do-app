# Task Manager Application

A task management application built with Python and Streamlit.

## Setup

1. Create and activate virtual environment:
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # Linux/Mac
   source env/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Features

- Create, edit, and delete tasks
- Organize tasks by category
- Set task priorities
- Mark tasks as completed
- Add reminders and labels
- Sort tasks by date, priority, or category
- View task statistics

## Design Patterns Implemented

1. **Factory Method Pattern**
   - Creates different types of tasks (standard and urgent)
   - Encapsulates task creation logic

2. **Decorator Pattern**
   - Adds features like reminders and labels to tasks
   - Maintains single responsibility principle

3. **Observer Pattern**
   - Notifies UI components when task status changes
   - Keeps UI in sync with task state

4. **Strategy Pattern**
   - Implements different sorting strategies
   - Easily switch between sorting methods

## Usage

1. **Adding Tasks**
   - Use the sidebar to add new tasks
   - Fill in the task details (title, category, priority)
   - Optionally add reminders and labels
   - Click "Add Task" to create the task

2. **Managing Tasks**
   - Check/uncheck tasks to mark them as complete/incomplete
   - Delete tasks using the delete button
   - Sort tasks using the dropdown menu

3. **Viewing Statistics**
   - View total tasks and completion rate
   - See task distribution by category

## Requirements

- Python 3.7+
- Streamlit
- python-dateutil 


## UML Diagram

- First install the Markdown Preview Mermaid Support for VS Code
- Then make right click on the README.md file and select "Open Preview"

```mermaid
classDiagram
    %% Enums
    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
    }

    %% Observer Pattern
    class Observer {
        <<abstract>>
        +update(task: Task)*
    }
    
    class Subject {
        -_observers: List[Observer]
        +__init__()
        +attach(observer: Observer)
        +detach(observer: Observer)
        +notify(task: Task)
    }

    %% Base Task
    class Task {
        +__init__(title: str, category: str, priority: Priority)
        +id: Optional[int]
        +title: str
        +category: str
        +priority: Priority
        +completed: bool
        +created_at: datetime
        +deadline: Optional[datetime]
        +mark_complete()
        +mark_incomplete()
        +set_deadline(deadline: datetime)
    }

    %% Factory Pattern
    class TaskFactory {
        <<abstract>>
        +create_task(title: str, category: str)*: Task
    }

    class StandardTaskFactory {
        +create_task(title: str, category: str): Task
    }

    class UrgentTaskFactory {
        +create_task(title: str, category: str): Task
    }

    %% Decorator Pattern
    class TaskDecorator {
        -_task: Task
        +__init__(task: Task)
        +id: Optional[int]
        +title: str
        +category: str
        +priority: Priority
        +completed: bool
        +created_at: datetime
        +deadline: Optional[datetime]
    }

    class ReminderDecorator {
        +reminder_time: datetime
        +__init__(task: Task, reminder_time: datetime)
    }

    class LabelDecorator {
        +label: str
        +__init__(task: Task, label: str)
    }

    %% Strategy Pattern
    class SortStrategy {
        <<abstract>>
        +sort(tasks: List[Task])*: List[Task]
    }

    class DateSortStrategy {
        +sort(tasks: List[Task]): List[Task]
    }

    class PrioritySortStrategy {
        +sort(tasks: List[Task]): List[Task]
    }

    class CategorySortStrategy {
        +sort(tasks: List[Task]): List[Task]
    }

    %% Task Manager
    class TaskManager {
        -tasks: List[Task]
        -_current_id: int
        -sort_strategy: SortStrategy
        +__init__()
        +add_task(task: Task)
        +remove_task(task_id: int)
        +get_tasks(): List[Task]
        +set_sort_strategy(strategy: SortStrategy)
        +get_task_by_id(task_id: int): Optional[Task]
    }

    %% Relationships
    Task --|> Subject : inherits
    Subject ..> Observer : notifies
    TaskFactory <|-- StandardTaskFactory : implements
    TaskFactory <|-- UrgentTaskFactory : implements
    Task <|-- TaskDecorator : extends
    TaskDecorator <|-- ReminderDecorator : extends
    TaskDecorator <|-- LabelDecorator : extends
    SortStrategy <|-- DateSortStrategy : implements
    SortStrategy <|-- PrioritySortStrategy : implements
    SortStrategy <|-- CategorySortStrategy : implements
    TaskManager o-- "0..*" Task : contains
    TaskManager o-- "1" SortStrategy : uses
    StandardTaskFactory ..> Task : creates
    UrgentTaskFactory ..> Task : creates
    Task --> Priority : has type 
```