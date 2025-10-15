from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from pydantic_ai import Agent, RunContext

from LearnPydanticAI.dependecies import TaskDependency
from LearnPydanticAI.model import TaskModel

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
                    """)
        
        return agent

    def run(self, query: str) -> str:
        deps = TaskDependency(username="sudo", project="LearnPydanticAI")
        result = self.agent.run_sync(query, deps=deps)
        return result.output
