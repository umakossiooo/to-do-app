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

1. Factory Method Pattern

    Design Problem:
    The system needed a way to create different types of tasks, such as standard and urgent tasks, without using conditional logic in multiple places.

    Pattern Reason:
    The Factory Method pattern helps encapsulate object creation. It allows defining a common interface for creating objects while letting subclasses decide which class to instantiate.

    Implemented Solution:
    An abstract class TaskFactory defines the method create_task. Subclasses like StandardTaskFactory and UrgentTaskFactory implement this method to return different task instances. This keeps task creation modular and extendable.

2. Decorator Pattern

    Design Problem:
    Tasks needed optional features like reminders and labels. Adding these features directly into the Task class would violate the single responsibility principle and make the class harder to maintain.

    Pattern Reason:
    The Decorator pattern allows adding extra behavior or data to individual objects without modifying their class. It supports flexible extension of functionalities.

    Implemented Solution:
    A base TaskDecorator class wraps a Task object. Subclasses such as ReminderDecorator and LabelDecorator add specific functionality (e.g., a reminder time or a custom label) to the task while maintaining the original interface.

3. Observer Pattern

    Design Problem:
    When a task's state changed (e.g., marked as completed), the system needed to update related components like the UI or a statistics counter.

    Pattern Reason:
    The Observer pattern defines a one-to-many relationship between objects. When one object changes, all its dependents are notified and updated automatically.

    Implemented Solution:
    The Task class extends a Subject class that maintains a list of observers. When a task is updated, it triggers the notify method, which calls the update method in each observer.

4. Strategy Pattern

    Design Problem:
    Tasks needed to be sorted by different criteria such as date, priority, or category. Hardcoding sorting logic made the system inflexible.

    Pattern Reason:
    The Strategy pattern allows defining a family of algorithms, encapsulating each one, and making them interchangeable. This supports flexible runtime behavior.

    Implemented Solution:
    An interface SortStrategy defines a sort method. Concrete classes like DateSortStrategy, PrioritySortStrategy, and CategorySortStrategy implement this method differently. The TaskManager selects the active sorting strategy and applies it to the task list.

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