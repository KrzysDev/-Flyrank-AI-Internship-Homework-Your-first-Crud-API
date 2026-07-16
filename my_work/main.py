from fastapi import FastAPI, HTTPException
from schemas.schemas import Task


all_tasks = []

app = FastAPI()


@app.get("/")
def information():
    return {"something": "here"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def tasks():
    return all_tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in all_tasks:
        if task.id == id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.post("/tasks")
def add_task(new_title: str):

    if new_title == "":
        raise HTTPException(
        status_code=404,
        detail=f"Name cannot be empty!"
    )

    last_id = all_tasks[len(all_tasks) - 1].id if len(all_tasks) > 0 else 0
    
    new_id = last_id + 1
    
    task = Task(
        id = new_id,
        title = new_title,
        done = False
    )

    all_tasks.append(task)

    return {"task appended status": "success"}


@app.put("/tasks/{id}")
def edit_task(id: int, task: Task):
    for i in range(len(all_tasks)):
        print(id, all_tasks[i].id)
        if int(id) == int(all_tasks[i].id):
            all_tasks[i] = task
            return {"edited task status": "success"}
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )



@app.delete("/tasks/{id}")
def delete_task(id: int):
    for i in range(len(all_tasks)):
        print(id, all_tasks[i].id)
        if int(id) == int(all_tasks[i].id):
            all_tasks.remove(all_tasks[i])
            return {"delete task status": "success"}
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )