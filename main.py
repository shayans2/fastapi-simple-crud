from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
from typing import List
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "Todo"

# Create
@app.post("/todo", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate):

    session = Session(bind=engine, expire_on_commit=False)
    tododb = models.ToDo(task = todo.task)

    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    session.close()

    return tododb

# Read
@app.get("/todo", response_model=List[schemas.ToDo], status_code=status.HTTP_200_OK)
def read_todo_list():

    session = Session(bind=engine, expire_on_commit=False)

    todo_list = session.query(models.ToDo).all()

    session.close()

    return todo_list

@app.get("/todo/{id}", response_model=schemas.ToDo, status_code=status.HTTP_200_OK)
def read_todo(id: int):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item not found")

    return todo

# Update
@app.put("/todo/{id}", response_model=schemas.ToDo, status_code=status.HTTP_200_OK)
def update_todo(id: int, task: str):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    if todo:
        todo.task = task
        session.commit()

    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo item not found")

    return todo

# Delete
@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    session = Session(bind=engine, expire_on_commit=False)

    todo = session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Todo item not found")

    return None
