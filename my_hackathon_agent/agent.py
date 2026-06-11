from http import client
import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
import smtplib
import sqlite3
import json
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
    # database start -------
def init_db():
    conn = sqlite3.connect('hackathon.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams 
                 (name TEXT, project TEXT, status TEXT)''')
    conn.commit()
    conn.close()
init_db()

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

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your functions ability.',
    tools=[Save_info, send_email],
)

