import asyncio
import os
from google.adk.agents import Agent
from google.adk.tools import AgentTool, google_search
import smtplib
import sqlite3
from email.message import EmailMessage

def send_email(to: str, title: str, message: str) -> str:
    """You can use this function to send an email. If the user does not provide all variables, you can ask them for the missing information."""

    Email_address = os.getenv("EMAIL_ADDRESS")
    Email_password = os.getenv("EMAIL_PASSWORD")
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = title
    msg['From'] = Email_address
    msg['To'] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(Email_address, Email_password)
            smtp.send_message(msg)
            return f"Email sent to {to} with title '{title}'"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

def Save_info(team_name: str, project: str, status: str) -> str:
    """You are a hackathon assistant. When a user asks about a team, always use the tool Save_info to get correct information."""
    # code for database connection and saving the information
    try:
        conn = sqlite3.connect('hackathon.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO teams (name, project, status) VALUES (?, ?, ?)", (team_name, project, status))
        conn.commit()
        conn.close()
        return f"Information of {team_name} saved in database!"
    except Exception as e:
        return f"Failed to save information: {str(e)}" 

db_agent = Agent(
    model='gemini-2.5-flash',
    name='db_agent',
    description='A helpful assistant for managing hackathon team information.',
    instruction='Answer user questions to the best of your functions ability.',
    tools=[Save_info, send_email],
)

research_agent = Agent(
    model='gemini-2.5-flash',
    name='research_specialist',
    instruction="You are an expert at finding information on the web. Use google_search to answer questions.",
    tools=[google_search]
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='orchestrator',
    instruction="""You are the leader of a team of agents. 
    1. If the user wants to save or view information about a team, send it to the database_specialist.
    2. If the user wants to know something about the world, send it to the research_specialist.
    Do not try to solve tasks yourself if you have a specialist available.""",
    tools=[
        AgentTool(db_agent), 
        AgentTool(research_agent)
    ]
)

async def main():
    # init db
    with sqlite3.connect('hackathon.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS teams (name TEXT PRIMARY KEY, project TEXT, status TEXT)')
    
    print("Agent team initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("\n🗣️ You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        # AWAIT is here - allows agents to work in the background while waiting for the response.
        print("🧠 Thinking...")
        response = await root_agent.run(user_input) 
        print(f"🤖 Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main()) # Starts directly the main function when the script is running.