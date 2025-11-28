# main.py
import os
import requests
from crewai import Agent, Task, Crew, LLM

def create_llm():
    return LLM(
        model="ollama/phi3",
        base_url="http://localhost:11434",
    )


def create_agent(topic):
    researcher = Agent(
        role=f"{topic} Researcher",
        goal=f"Find the latest discoveries and inventions in {topic}",
        backstory=f"A talented researcher who finds the newest innovations in {topic}",
        verbose=True,
        allow_delegation=True,
        llm=create_llm(),
    )

    writer = Agent(
        role="LinkedIn Post Writer",
        goal=f"Write a polished LinkedIn post about {topic}",
        backstory="A professional LinkedIn content writer",
        verbose=True,
        llm=create_llm(),
    )

    return researcher, writer


def create_task(topic, researcher, writer):
    research_task = Task(
        description=f"Research new breakthroughs in {topic}",
        expected_output="8–12 lines of research summary",
        agent=researcher,
    )

    writer_task = Task(
        description="Write a clean LinkedIn post based on the research summary without any personal pronouns and the maximum number of characters should not exceed 3000",
        expected_output="Summary of research topic in a file not more than 3000 characters",
        agent=writer,
        context=[research_task],
        output_file = "content.md"
    )

    return research_task, writer_task


def create_crew(topic):
    researcher, writer= create_agent(topic)
    research_task, writer_task = create_task(topic, researcher, writer)

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writer_task],
        verbose=True
    )

    return crew.kickoff()


if __name__ == "__main__":
    topic = "Artificial Intelligence"
    result = create_crew(topic)
    with open("content.md", "r") as f:
        content = f.read()
    webhook_url = "https://kabilkirithik.app.n8n.cloud/webhook-test/926cd37b-b8c1-4a63-bac3-5bd8dfb2b49c"
    payload = {
                "post_content": content
            }
    try:
        response = requests.post(
        webhook_url,
            json=payload,
            timeout=15
                )
        if response.status_code in [200,201,202]:
            print("success, webhook posted")
        else:
            print("webhook failed to post")
    except Exception as e:
        print("Webhook failed reason",e) 

    print("\n======== FINAL RESULT ========\n")
    print(result)      # <-- FIXED (no json.dumps)
