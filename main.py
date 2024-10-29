# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(
    title="Todo API",
    description="A simple Todo API service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/tododb")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class TodoItem(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class TodoCreate(BaseModel):
    title: str
    description: str = None

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Routes
@app.post("/todos/", response_model=TodoResponse, tags=["todos"])
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item"""
    db_todo = TodoItem(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=list[TodoResponse], tags=["todos"])
async def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all todo items"""
    return db.query(TodoItem).offset(skip).limit(limit).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo item"""
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo item"""
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item"""
    db_todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return db_todo

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)