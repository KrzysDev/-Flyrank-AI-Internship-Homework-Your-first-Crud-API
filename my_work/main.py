import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Response, status
from schemas.schemas import Task, TaskCreate, TaskUpdate

all_tasks = [
    Task(id=1, title="Buy milk", done=False),
    Task(id=2, title="Clean the room", done=True),
    Task(id=3, title="Read a book", done=False),
]

app = FastAPI()


@app.get("/")
def information():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def tasks(search: str | None = None, done: bool | None = None):
    
    def meets_criteria(task: Task):
        if search is not None and search not in task.title:
            return False

        if done is not None and task.done != done:
            return False

        return True
    
    if len(all_tasks) > 0:
        res = filter(meets_criteria, all_tasks)
        return list(res)
    else:
        return all_tasks
        
@app.get("/stats")
def stats():
    open_tasks = tasks(done=False)
    closed_tasks = tasks(done=True)

    return {
        "total": len(all_tasks),
        "done": len(closed_tasks),
        "open": len(open_tasks)
    }
    


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in all_tasks:
        if task.id == id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {id} not found"
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def add_task(payload: TaskCreate):
    if not payload.title or payload.title.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    last_id = all_tasks[-1].id if len(all_tasks) > 0 else 0
    new_id = last_id + 1
    
    new_task = Task(
        id=new_id,
        title=payload.title,
        done=False
    )
    all_tasks.append(new_task)
    return new_task


@app.put("/tasks/{id}")
def edit_task(id: int, payload: TaskUpdate):
    for task in all_tasks:
        if task.id == id:
            if payload.title is not None and payload.title.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Title cannot be empty"
                )
            
            if payload.title is not None:
                task.title = payload.title
            if payload.done is not None:
                task.done = payload.done
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {id} not found"
    )


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    for i in range(len(all_tasks)):
        if all_tasks[i].id == id:
            all_tasks.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {id} not found"
    )


@app.post("/reset")
def reset_tasks():
    all_tasks.clear()
    all_tasks.extend([Task(id=1, title="Buy milk", done=False), Task(id=2, title="Clean the room", done=True), Task(id=3, title="Read a book", done=False)])
    return {"message": "Tasks reset to default state"}
