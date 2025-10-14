from dotenv import load_dotenv
from LearnPydanticAI.agent import TaskAgent


load_dotenv()  # take environment variables from .env.

agent = TaskAgent()
answer = agent.run("I want to learn more about Pydantic AI.")
print(answer)