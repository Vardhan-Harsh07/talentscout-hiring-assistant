from dotenv import load_dotenv
import os
import requests

# Load your token
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
