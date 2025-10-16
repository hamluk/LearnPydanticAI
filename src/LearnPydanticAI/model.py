from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    task: str = Field(description="The title of the task.")
    description: str = Field(description="A brief description of the task specifing its steps.")
    priority: int = Field(description="The priority of the task on a scale from 1 (high) to 5 (low).")
    project: str = Field(description="The project the task belongs to.")
    created_by:str = Field(description="The name of the person who created the task.")
    number_of_open_tasks: int = Field(description="The number of open tasks for the project after creating this task.")
    success: bool = Field(description="Indicates if the task was created successfully.")