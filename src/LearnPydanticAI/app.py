from dotenv import load_dotenv
from LearnPydanticAI.agent import TaskAgent
from LearnPydanticAI.session import AgentSession
from LearnPydanticAI.dependecies import TaskDependency


load_dotenv()  # take environment variables from .env.

agent = TaskAgent()
session = AgentSession(agent.agent)
deps = TaskDependency(username="sudo", project="LearnPydanticAI")

answer1 = session.run(query="I want to learn more about Pydantic AI.", deps=deps)
print(answer1)
print()

answer2 = session.run(query="Update its creator to joe", deps=deps)
print(answer2)
