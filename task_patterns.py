from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from enum import Enum

# Task Priority Enum
class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self, task: 'Task') -> None:
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, task: 'Task') -> None:
        for observer in self._observers:
            observer.update(task)

# Base Task
class Task(Subject):
    def __init__(self, title: str, category: str, priority: Priority = Priority.MEDIUM):
        super().__init__()
        self.id: Optional[int] = None
        self.title = title
        self.category = category
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
        self.deadline: Optional[datetime] = None

    def mark_complete(self):
        self.completed = True
        self.notify(self)

    def mark_incomplete(self):
        self.completed = False
        self.notify(self)

    def set_deadline(self, deadline: datetime):
        self.deadline = deadline
        self.notify(self)

# Factory Method Pattern
class TaskFactory(ABC):
    @abstractmethod
    def create_task(self, title: str, category: str) -> Task:
        pass

class StandardTaskFactory(TaskFactory):
    def create_task(self, title: str, category: str) -> Task:
        return Task(title, category, Priority.MEDIUM)

class UrgentTaskFactory(TaskFactory):
    def create_task(self, title: str, category: str) -> Task:
        task = Task(title, category, Priority.HIGH)
        return task

# Decorator Pattern
class TaskDecorator(Task):
    def __init__(self, task: Task):
        self._task = task
        super().__init__(task.title, task.category, task.priority)
        self.id = task.id
        self.completed = task.completed
        self.created_at = task.created_at
        self.deadline = task.deadline

class ReminderDecorator(TaskDecorator):
    def __init__(self, task: Task, reminder_time: datetime):
        super().__init__(task)
        self.reminder_time = reminder_time

class LabelDecorator(TaskDecorator):
    def __init__(self, task: Task, label: str):
        super().__init__(task)
        self.label = label

# Strategy Pattern
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, tasks: List[Task]) -> List[Task]:
        pass

class DateSortStrategy(SortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda x: x.created_at)

class PrioritySortStrategy(SortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(tasks, key=lambda x: priority_order[x.priority])

class CategorySortStrategy(SortStrategy):
    def sort(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda x: x.category)

# Task Manager
class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self._current_id = 0
        self.sort_strategy: SortStrategy = DateSortStrategy()

    def add_task(self, task: Task) -> None:
        self._current_id += 1
        task.id = self._current_id
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_tasks(self) -> List[Task]:
        return self.sort_strategy.sort(self.tasks)

    def set_sort_strategy(self, strategy: SortStrategy) -> None:
        self.sort_strategy = strategy

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None 