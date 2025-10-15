from dataclasses import dataclass


@dataclass
class TaskDependency:
    username: str
    project: str