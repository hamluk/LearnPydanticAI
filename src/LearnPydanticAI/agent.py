from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai import Agent, RunContext

from LearnPydanticAI.dependecies import TaskDependency
from LearnPydanticAI.model import TaskModel
from LearnPydanticAI.data import PROJECTS

import os


class TaskAgent():
    def __init__(self):
        self.agent = self._init_agent()
    
    def _init_agent(self) -> Agent:
        agent = Agent(
            model = MistralModel(model_name=os.getenv("LLM_MISTRAL_MODEL"), provider=MistralProvider(api_key=os.getenv("MISTRAL_API_KEY"))),
            output_type=TaskModel,
            deps_type=TaskDependency,
            )
        
        @agent.system_prompt
        def create_system_prompt(ctx: RunContext[TaskDependency]) -> str:
            return (f"""
                    Create a brief task from the user's request. 
                    The task is created by {ctx.deps.username}.
                    The taks belongs to the project {ctx.deps.project}.
                    Before creating the task verify that the project {ctx.deps.project} exists by retrieving project details.
                    If you sucessfully verified that it exists update the number of open tasks for this project.
                    If the project does not exists, mark the task creation as failed and leave the task and its desciprtion empty.
                    """)
        
        @agent.tool_plain
        def get_project_info(project_name: str) -> str:
            """Retrieves project information"""
            project = PROJECTS.get(project_name, None)
            if not project:
                return f"Project {project_name} not found."
            return project
        
        @agent.tool_plain
        def update_open_tasks(project_name: str, new_open_tasks) -> str:
            """Updates the number of open tasks for a given project."""
            project = PROJECTS.get(project_name, None)
            if not project:
                return f"Updating open tasks failed for project {project_name}. Project does not exist."

            project["open_tasks"] = new_open_tasks
            return f"Sucessfully updated open tasks for project {project_name} to {project["open_tasks"]}."
           
        return agent

    def run(self, query: str, deps) -> str:
        result = self.agent.run_sync(query, deps=deps)
        # Bonus for inspection function calls
        # for message in result.all_messages():
        #     print(message)
        return result.output
