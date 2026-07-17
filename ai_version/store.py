"""In-memory task store with seed/reset support."""

from models import TaskStatus


# ── In-memory storage ────────────────────────────────────────────────
_tasks: dict[int, dict] = {}
_next_id: int = 1

SEED_TASKS = [
    {"title": "Buy milk", "description": "Get 2% milk from the store", "status": TaskStatus.OPEN},
    {"title": "Write report", "description": "Finish the Q3 summary report", "status": TaskStatus.DONE},
    {"title": "Call dentist", "description": "Schedule a checkup appointment", "status": TaskStatus.OPEN},
]


def _reset_id_counter() -> None:
    global _next_id
    _next_id = 1


def _allocate_id() -> int:
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


# ── CRUD helpers ─────────────────────────────────────────────────────

def list_tasks() -> list[dict]:
    """Return all tasks as a list."""
    return list(_tasks.values())


def get_task(task_id: int) -> dict | None:
    return _tasks.get(task_id)


def create_task(title: str, description: str | None, status: TaskStatus) -> dict:
    task_id = _allocate_id()
    task = {"id": task_id, "title": title, "description": description, "status": status}
    _tasks[task_id] = task
    return task


def update_task(task_id: int, **fields) -> dict | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    for key, value in fields.items():
        if value is not None:
            task[key] = value
    return task


def delete_task(task_id: int) -> dict | None:
    return _tasks.pop(task_id, None)


# ── Seed & reset ─────────────────────────────────────────────────────

def seed() -> list[dict]:
    """Add the 3 example tasks (without clearing existing ones)."""
    created = []
    for t in SEED_TASKS:
        created.append(create_task(t["title"], t["description"], t["status"]))
    return created


def reset() -> list[dict]:
    """Clear everything and re-seed with the 3 example tasks."""
    _tasks.clear()
    _reset_id_counter()
    return seed()
