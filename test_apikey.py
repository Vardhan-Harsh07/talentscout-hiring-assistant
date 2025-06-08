from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize the client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple prompt to test if API is working
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say Hello World"}
        ],
        temperature=0.5
    )
    print("✅ Response from OpenAI:")
    print(response.choices[0].message.content)

except Exception as e:
    print("❌ Error from OpenAI API:")
    print(e)
