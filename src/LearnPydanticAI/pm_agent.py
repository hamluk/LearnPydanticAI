from pydantic_ai import Agent
from pydantic_ai.models.mistral import MistralModel
from pydantic_ai.providers.mistral import MistralProvider
from LearnPydanticAI.data import PROJECTS
from LearnPydanticAI.model import Failed, ProjectDetails

import os


class ProjectManagementAgent:
    def __init__(self):
        self.agent = self._init_agent()

    def _init_agent(self) -> Agent[ProjectDetails | Failed, None]:
        agent = Agent[ProjectDetails | Failed, None](
            model = MistralModel(model_name=os.getenv("LLM_MISTRAL_MODEL"), provider=MistralProvider(api_key=os.getenv("MISTRAL_API_KEY"))),
            output_type=ProjectDetails | Failed,
            system_prompt=("""
                           You are a project management agent having the task to update the open numbers of tasks for a project. 
                           """)
            )
        
        @agent.tool_plain
        def update_open_tasks(project_name: str) -> ProjectDetails | Failed:
            """Updates the number of open tasks for a given project."""
            project = PROJECTS.get(project_name, None)
            if project is None:
                return Failed(reason=f"Updating open tasks failed for project {project_name}. Project does not exist.")

            # create internal ProjectDetails python object and increase number of open tasks by one
            project_details = ProjectDetails(owned_by_group=project.get("group"), number_of_open_tasks=project.get("open_tasks"))
            project_details.number_of_open_tasks += 1

            # write the new project details back to the data
            # this reflects a database update instruction for a real-world application
            project["open_tasks"] = project_details.number_of_open_tasks
            
            return project_details
        
        return agent
        
    async def run(self, query: str) -> ProjectDetails | Failed:
        result = await self.agent.run(query)

        # Bonus for inspection function calls
        # print("**** Project Management Agent Call Trace ****")
        # for message in result.all_messages():
        #     print(message)
        #     print("-----")

        return result.output