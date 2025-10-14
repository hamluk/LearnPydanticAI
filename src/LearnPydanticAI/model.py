from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    task: str = Field(description="The title of the task.")
    description: str = Field(description="A brief description of the task specifing its steps.")
    priority: int = Field(description="The priority of the task on a scale from 1 (high) to 5 (low).")