from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def information():
    return {"something" : "here"}

@app.get("/health")
def health():
    return {"status" : "ok"}

@app.get("/tasks")
def tasks():
    pass

@app.get("/tasks/{id}")
def get_task(id):
    pass

@app.post("/tasks")
def add_task():
    pass

@app.post("/tasks/{id}")
def edit_task(id):
    pass

@app.delete("/tasks/{id}")
def delete_task(id):
    pass
