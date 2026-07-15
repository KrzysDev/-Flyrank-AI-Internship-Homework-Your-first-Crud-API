from fastapi import FastAPI
from schemas.schemas import Task

app = FastAPI()

tasks: list[Task] = []

@app.get("/")
def information():
    return {"something" : "here"}

@app.get("/health")
def health():
    return {"status" : "ok"}

@app.get("/tasks")
def tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id):
    for task in tasks:
        if task.id == id:
            return task


@app.post("/tasks")
def add_task():
    pass

@app.post("/tasks/{id}")
def edit_task(id):
    pass

@app.delete("/tasks/{id}")
def delete_task(id):
    pass
