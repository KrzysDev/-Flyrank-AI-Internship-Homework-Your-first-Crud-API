from fastapi import FastAPI
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
def get_task(id):
    for task in all_tasks:
        if task.id == id:
            return task


@app.post("/tasks")
def add_task(title: str):
    task = Task()

    task.title = title

    last_id = tasks[len(tasks) - 1].id
    
    task.id = last_id + 1

    task.done = False

    all_tasks.append(task)
    
    return {"task appended status": "success"}


@app.put("/tasks/{id}")
def edit_task(id, task: Task):
    for i in range(len(all_tasks)):
        print(id, all_tasks[i].id)
        if int(id) == int(all_tasks[i].id):
            all_tasks[i] = task
            return {"edited task status": "success"}


@app.delete("/tasks/{id}")
def delete_task(id):
    pass