import os
from google.adk.agents.llm_agent import Agent
import smtplib
from email.message import EmailMessage

def send_email(to: str, title: str, message: str) -> str:
    """You can use this function to send an email."""

    Email_address = os.getenv("EMAIL_ADDRESS")
    Email_password = os.getenv("EMAIL_PASSWORD")
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = title
    msg['From'] = Email_address
    msg['To'] = to

    try:
        with smtplib.SMTP("://gmail.com", 465) as smtp:
            smtp.login(Email_address, Email_password)
            smtp.send_message(msg)
            return f"Email sent to {to} with title '{title}'"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

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

