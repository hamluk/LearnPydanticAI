from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai import Agent, RunContext
from LearnPydanticAI.dependecies import TaskDependency
from LearnPydanticAI.model import Failed, TaskModel
from LearnPydanticAI.pm_agent import ProjectManagementAgent

import os


class TaskAgent():
    def __init__(self):
        self.agent = self._init_agent()
        self.pm_agent = ProjectManagementAgent()
    
    def _init_agent(self) -> Agent:
        agent = Agent(
            model = MistralModel(model_name=os.getenv("LLM_MISTRAL_MODEL"), provider=MistralProvider(api_key=os.getenv("MISTRAL_API_KEY"))),
            output_type=TaskModel | Failed,
            deps_type=TaskDependency,
            )
        
        @agent.system_prompt
        def create_system_prompt(ctx: RunContext[TaskDependency]) -> str:
            return (f"""
                    You are a task creation agent.
                    Always follow the following instructions:
                    1. Update the project {ctx.deps.project} using the 'update_project' tool
                    2. Create a brief task from the user's query. It is created by {ctx.deps.username} and belongs to the project {ctx.deps.project}.
                    """)
        
        @agent.tool_plain
        async def update_project(project_name: str) -> str:
            """Update the new created tasks project."""
            result = await self.pm_agent.run(query=f"Update open tasks for {project_name}")

            if isinstance(result, Failed):
                return Failed(reason=f"Task creation failed: {result.reason}")
            
            return f"Updated project details for project {project_name}: {result}."
           
        return agent

    async def run(self, query: str, deps: TaskDependency) -> str:
        result = await self.agent.run(query, deps=deps)

        # Bonus for inspection function calls
        # print("**** Task Agent Call Trace ****")
        # for message in result.all_messages():
        #     print(message)
        #     print("-----")

        return result.output
