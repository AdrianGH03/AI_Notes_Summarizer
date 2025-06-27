from typing import List, Optional
from enum import IntEnum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    low = 3
    medium = 2
    high = 1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo item")
    todo_description: str = Field(..., description="Description of the todo item")
    priority: Priority = Field(default=Priority.low, description="Priority of the todo item")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier for the todo item")


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Updated name of the todo item")
    todo_description: Optional[str] = Field(None, description="Updated description of the todo item")
    priority: Optional[Priority] = Field(None, description="Updated priority of the todo item")


all_todos = [
    Todo(todo_id=1, todo_name='Buy groceries', todo_description='Milk, Bread, Eggs', priority=Priority.medium),
    Todo(todo_id=2, todo_name='Walk the dog', todo_description='Evening walk at the park', priority=Priority.low),
    Todo(todo_id=3, todo_name='Read a book', todo_description='Finish reading "1984" by George Orwell', priority=Priority.high),
    Todo(todo_id=4, todo_name='Exercise', todo_description='30 minutes of cardio', priority=Priority.medium),
    Todo(todo_id=5, todo_name='Clean the house', todo_description='Vacuum and dust all rooms', priority=Priority.low)
]

#GET, POST, PUT, DELETE

@api.get('/todos/{todo_id}', response_model=Todo)
async def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    
    raise HTTPException(status_code=404, detail="Todo not found")
        
@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
        
    
@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1
    new_todo = Todo(todo_id=new_todo_id,
                    todo_name=todo.todo_name,
                    todo_description=todo.todo_description,
                    priority=todo.priority)
        
    all_todos.append(new_todo)

    return new_todo

@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
        
    raise HTTPException(status_code=404, detail="Todo not found")
    
@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo = all_todos.pop(index)
            return deleted_todo
    
    raise HTTPException(status_code=404, detail="Todo not found")


        