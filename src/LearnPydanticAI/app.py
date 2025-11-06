from dotenv import load_dotenv
from LearnPydanticAI.task_agent import TaskAgent
from LearnPydanticAI.dependecies import TaskDependency

import asyncio

async def main():
    load_dotenv()  # take environment variables from .env.

    agent = TaskAgent()

    # successful run
    deps = TaskDependency(username="sudo", project="LearnPydanticAI")
    answer = await agent.run("I want to learn more about Pydantic AI.", deps=deps)
    print(answer)

    # failed run due to a non-existing project
    deps_fail = TaskDependency(username="sudo", project="NonExistingProject")
    failed_answer = await agent.run("I want to learn more about Pydantic AI.", deps=deps_fail)
    print(failed_answer)

if __name__ == "__main__":
    asyncio.run(main())