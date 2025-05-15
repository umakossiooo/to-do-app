import streamlit as st
from datetime import datetime, timedelta
from task_patterns import (
    TaskManager, Task, Priority, StandardTaskFactory, UrgentTaskFactory,
    ReminderDecorator, LabelDecorator, DateSortStrategy, PrioritySortStrategy,
    CategorySortStrategy
)

# Initialize session state
if 'task_manager' not in st.session_state:
    st.session_state.task_manager = TaskManager()

# Page config
st.set_page_config(page_title="Task Manager", layout="wide")
st.title("📝 Task Manager")

# Sidebar for adding tasks
with st.sidebar:
    st.header("Add New Task")
    task_title = st.text_input("Task Title")
    task_category = st.selectbox("Category", ["Personal", "Work", "Shopping", "Other"])
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    is_urgent = st.checkbox("Mark as Urgent")
    add_reminder = st.checkbox("Add Reminder")
    add_label = st.checkbox("Add Label")
    
    if add_reminder:
        reminder_date = st.date_input("Reminder Date")
        reminder_time = st.time_input("Reminder Time")
        reminder_datetime = datetime.combine(reminder_date, reminder_time)
    
    if add_label:
        label_text = st.text_input("Label")
    
    if st.button("Add Task"):
        if task_title:
            # Create task using factory pattern
            factory = UrgentTaskFactory() if is_urgent else StandardTaskFactory()
            task = factory.create_task(task_title, task_category)
            task.priority = Priority[task_priority.upper()]
            
            # Add decorators if needed
            if add_reminder:
                task = ReminderDecorator(task, reminder_datetime)
            if add_label and label_text:
                task = LabelDecorator(task, label_text)
            
            st.session_state.task_manager.add_task(task)
            st.success("Task added successfully!")
        else:
            st.error("Please enter a task title!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Tasks")
    # Sorting options
    sort_method = st.selectbox(
        "Sort by",
        ["Date", "Priority", "Category"],
        key="sort_method"
    )
    
    # Apply sorting strategy
    if sort_method == "Date":
        st.session_state.task_manager.set_sort_strategy(DateSortStrategy())
    elif sort_method == "Priority":
        st.session_state.task_manager.set_sort_strategy(PrioritySortStrategy())
    else:
        st.session_state.task_manager.set_sort_strategy(CategorySortStrategy())

    # Display tasks
    tasks = st.session_state.task_manager.get_tasks()
    for task in tasks:
        with st.container():
            col_check, col_content, col_actions = st.columns([0.1, 0.7, 0.2])
            
            with col_check:
                if st.checkbox("", task.completed, key=f"check_{task.id}"):
                    if not task.completed:
                        task.mark_complete()
                else:
                    if task.completed:
                        task.mark_incomplete()
            
            with col_content:
                title_text = f"~~{task.title}~~" if task.completed else task.title
                st.markdown(f"**{title_text}**")
                st.caption(f"Category: {task.category} | Priority: {task.priority.value}")
                
                # Show decorator information
                if isinstance(task, ReminderDecorator):
                    st.caption(f"🔔 Reminder: {task.reminder_time.strftime('%Y-%m-%d %H:%M')}")
                if isinstance(task, LabelDecorator):
                    st.caption(f"🏷️ Label: {task.label}")
            
            with col_actions:
                if st.button("Delete", key=f"delete_{task.id}"):
                    st.session_state.task_manager.remove_task(task.id)
                    st.rerun()

with col2:
    st.subheader("Statistics")
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.completed])
    
    st.metric("Total Tasks", total_tasks)
    st.metric("Completed Tasks", completed_tasks)
    if total_tasks > 0:
        st.metric("Completion Rate", f"{(completed_tasks/total_tasks)*100:.1f}%")
    
    # Category breakdown
    st.subheader("Categories")
    categories = {}
    for task in tasks:
        categories[task.category] = categories.get(task.category, 0) + 1
    
    for category, count in categories.items():
        st.text(f"{category}: {count} tasks") 