from google.adk.agents.llm_agent import Agent

def hamta_status(team_namn: str) -> str:
    """"Du är en hackathon-assistent. Om användaren frågar om ett team, använd ALLTID verktyget hämta_status för att få rätt information."""
    # Här kan du ha kod som kollar en databas eller en hemsida
    return f"Team {team_namn} är just nu i full gång med att bygga sin agent!"

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your functions ability.',
    tools=[hamta_status],
)

