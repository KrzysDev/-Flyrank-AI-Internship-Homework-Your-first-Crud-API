"""Pydantic models for the Todo API."""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Possible statuses for a task."""
    OPEN = "open"
    DONE = "done"


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the task")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    status: TaskStatus = Field(TaskStatus.OPEN, description="Status of the task")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None


class TaskOut(BaseModel):
    """Schema for task responses."""
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus


class StatsOut(BaseModel):
    """Schema for the /tasks/stats endpoint."""
    total: int
    done: int
    open: int
