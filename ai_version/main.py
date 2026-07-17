"""
Todo List API — FastAPI + in-memory storage.

Run with:
    uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException, Query
from typing import Optional

from models import TaskCreate, TaskUpdate, TaskOut, StatsOut, TaskStatus
import store

app = FastAPI(
    title="Todo List API",
    description="A simple CRUD API for managing a todo list (in-memory, no database).",
    version="1.0.0",
)


# ── Lifecycle: seed on startup ───────────────────────────────────────

@app.on_event("startup")
def startup_seed():
    """Populate the store with example tasks when the server starts."""
    store.seed()


# ── Stats ────────────────────────────────────────────────────────────

@app.get("/tasks/stats", response_model=StatsOut, tags=["Stats"])
def get_stats():
    """Return counts: total, done, and open tasks."""
    tasks = store.list_tasks()
    total = len(tasks)
    done = sum(1 for t in tasks if t["status"] == TaskStatus.DONE)
    return StatsOut(total=total, done=done, open=total - done)


# ── Seed & Reset ─────────────────────────────────────────────────────

@app.post("/tasks/seed", response_model=list[TaskOut], tags=["Seed & Reset"])
def seed_tasks():
    """Append the 3 example tasks to the current store."""
    return store.seed()


@app.post("/tasks/reset", response_model=list[TaskOut], tags=["Seed & Reset"])
def reset_tasks():
    """Clear all tasks and restore the 3 example tasks (IDs restart from 1)."""
    return store.reset()


# ── CRUD ─────────────────────────────────────────────────────────────

@app.get("/tasks", response_model=list[TaskOut], tags=["Tasks"])
def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status (open / done)"),
    search: Optional[str] = Query(None, description="Search in title and description"),
):
    """
    List all tasks.

    Supports optional query parameters:
    - **status** — filter by `open` or `done`
    - **search** — case-insensitive substring search across title & description
    """
    tasks = store.list_tasks()

    if status is not None:
        tasks = [t for t in tasks if t["status"] == status]

    if search is not None:
        search_lower = search.lower()
        tasks = [
            t for t in tasks
            if search_lower in t["title"].lower()
            or (t["description"] and search_lower in t["description"].lower())
        ]

    return tasks


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def get_task(task_id: int):
    """Get a single task by its ID."""
    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", response_model=TaskOut, status_code=201, tags=["Tasks"])
def create_task(body: TaskCreate):
    """Create a new task."""
    return store.create_task(
        title=body.title,
        description=body.description,
        status=body.status,
    )


@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def update_task(task_id: int, body: TaskUpdate):
    """Update an existing task (partial update — only supplied fields are changed)."""
    updated = store.update_task(
        task_id,
        title=body.title,
        description=body.description,
        status=body.status,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return updated


@app.delete("/tasks/{task_id}", response_model=TaskOut, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task by its ID. Returns the deleted task."""
    deleted = store.delete_task(task_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return deleted
