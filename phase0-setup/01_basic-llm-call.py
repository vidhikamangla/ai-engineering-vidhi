import os

from dotenv import load_dotenv
from google import genai

#GEMINI_API_KEY in .env file 
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

question = input("Ask something: ")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=question,
)
print(response.text)

# ----------------------------------------------------

#Call with system instruction
# question2= input("Ask something, to a backend eng lead: ")
