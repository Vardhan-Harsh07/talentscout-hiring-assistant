# from dotenv import load_dotenv
# import os
# import requests

# # Load environment variables
# load_dotenv()
# hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# # Use a hosted instruction-tuned model
# MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
# API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

# HEADERS = {
#     "Authorization": f"Bearer {hf_token}",
#     "Content-Type": "application/json"
# }

# def generate_greeting():
#     return "👋 Hello! I'm TalentScout, your intelligent hiring assistant. I'll ask you a few questions to get started."

# def generate_questions(tech_stack):
#     # Clean and format the tech stack
#     if not tech_stack or tech_stack.strip() == "":
#         tech_stack = "General Programming"
    
#     tech_stack = tech_stack.strip()
    
#     prompt = (
#         f"Generate 4 practical technical interview questions for a candidate skilled in {tech_stack} technology. "
#         "Format your response as a numbered list (1. 2. 3. 4.). "
#         "Each question should be clear, concise, and focused on practical skills. "
#         "For database technologies like SQL, focus on queries, optimization, and design. "
#         "For programming languages, focus on coding problems and best practices. "
#         "For frameworks, focus on implementation and architecture. "
#         "Provide realistic scenarios for each question. "
#         "Do not include answers, explanations, or additional text - only the 4 numbered questions."
#     )

#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "temperature": 0.6,
#             "max_new_tokens": 1000,
#             "return_full_text": False
#         }
#     }

#     # rest of your code


#     try:
#         response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
#         response.raise_for_status()
#         output = response.json()

#         if isinstance(output, list):
#             content = output[0].get("generated_text", "").strip()

#             # Debug print (optional)
#             print("🔍 DEBUG: Raw output:\n", content)

#             # Only treat it as valid if there's some meaningful content
#             if content and content.startswith("Q1"):
#                 return content
#             elif content:
#                 return content + "\n⚠️ Note: Response may be incomplete or not in expected format."
#             else:
#                 return "⚠️ No questions generated."
#         else:
#             return "⚠️ Unexpected response format."

#     except requests.exceptions.HTTPError as http_err:
#         return f"HTTP error occurred: {http_err} - {response.text}"
#     except requests.exceptions.RequestException as req_err:
#         return f"Request error: {req_err}"
#     except Exception as e:
#         return f"⚠️ An unexpected error occurred: {str(e)}"
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Use a hosted instruction-tuned model
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

HEADERS = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

def generate_greeting():
    return "👋 Hello! I'm TalentScout, your intelligent hiring assistant. I'll ask you a few questions to get started."

def generate_fallback_questions(tech_stack):
    """Generate fallback questions when API fails"""
    tech_stack_lower = tech_stack.lower().strip()
    
    if 'java' in tech_stack_lower:
        return """1. Design a simple REST API for a library management system using Spring Boot. What endpoints would you create and what HTTP methods would you use?

2. You have a list of 10,000 employee records that need to be processed. How would you implement this efficiently in Java, and what would you consider for memory management?

3. Explain how you would implement exception handling in a Java application that reads data from a file and saves it to a database.

4. Write a method that finds the second largest number in an array of integers. What edge cases would you need to handle?"""
    
    elif 'sql' in tech_stack_lower:
        return """1. Design a database schema for an e-commerce platform with products, customers, and orders. Show the relationships between tables.

2. Write a query to find the top 5 customers who have spent the most money in the last 6 months.

3. You have a slow-running query that joins 3 large tables. What steps would you take to optimize its performance?

4. Explain the difference between INNER JOIN and LEFT JOIN with a practical example."""
    
    elif 'python' in tech_stack_lower:
        return """1. Create a function that reads a CSV file with 1 million records and processes them efficiently without running out of memory.

2. You need to build a simple web scraper that extracts product prices from an e-commerce site. What libraries would you use and how would you handle rate limiting?

3. Implement a decorator that logs the execution time of any function. Show how you would use it.

4. Design a class structure for a simple banking system with accounts, transactions, and customers."""
    
    elif 'javascript' in tech_stack_lower or 'js' in tech_stack_lower or 'node' in tech_stack_lower:
        return """1. Create a function that debounces API calls when a user types in a search box. Explain why this is important.

2. You have an array of user objects and need to group them by their department. How would you implement this efficiently?

3. Build a simple promise-based function that fetches data from multiple APIs concurrently and handles errors gracefully.

4. Explain how you would implement form validation for a user registration form with real-time feedback."""
    
    elif 'react' in tech_stack_lower:
        return """1. Create a reusable component that displays a list of items with pagination. What props would it accept?

2. You have a form with 10 input fields. How would you manage the state efficiently and handle form submission?

3. Implement a custom hook that fetches data from an API and handles loading states and errors.

4. Explain how you would optimize a React component that renders a large list of items (1000+ items)."""
    
    elif 'php' in tech_stack_lower:
        return """1. Create a secure login system in PHP that handles user authentication and password hashing. What security measures would you implement?

2. You need to build a file upload feature that handles multiple file types and sizes. How would you implement validation and security?

3. Design a simple MVC structure for a blog application. Explain how the components would interact.

4. Write a function that connects to a MySQL database and safely executes queries to prevent SQL injection."""
    
    elif 'c#' in tech_stack_lower or 'csharp' in tech_stack_lower or '.net' in tech_stack_lower:
        return """1. Create a Web API controller that handles CRUD operations for a Product entity. What attributes and methods would you include?

2. Implement dependency injection in a .NET application for a service that handles email notifications.

3. You have a performance issue with Entity Framework queries. What optimization techniques would you apply?

4. Design a background service that processes messages from a queue. How would you handle errors and retries?"""
    
    else:
        return f"""1. Describe how you would approach building a new feature in {tech_stack}. What would be your first steps and considerations?

2. You encounter a performance bottleneck in a {tech_stack} application. What tools and techniques would you use to identify and resolve it?

3. How would you implement comprehensive error handling and logging in a {tech_stack} project?

4. Explain how you would structure a {tech_stack} project for maintainability, scalability, and team collaboration."""

def generate_questions(tech_stack):
    # Clean and format the tech stack
    if not tech_stack or tech_stack.strip() == "":
        tech_stack = "General Programming"
    
    tech_stack = tech_stack.strip()
    
    print(f"🔍 DEBUG: Generating questions for: '{tech_stack}'")
    
    # Try API first, but immediately fall back on any error
    try:
        prompt = (
    f"Generate 4 practical technical interview questions for a candidate skilled in {tech_stack}. "
    f"Each question should be unique, clear, and based on real-world scenarios. "
    f"Respond with only the following numbered format:\n"
    f"1. <question one>\n"
    f"2. <question two>\n"
    f"3. <question three>\n"
    f"4. <question four>\n"
    f"strictly Do not include any introductions, explanations, markdown formatting, or extra text. Only return the 4 questions."
)



        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.6,
                "max_new_tokens": 300,
                "return_full_text": False
            }
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=90)
        
        # If API call succeeds, process the response
        if response.status_code == 200:
            output = response.json()
            print(f"🔍 DEBUG: API Response: {output}")
            
            if isinstance(output, list) and len(output) > 0:
                content = output[0].get("generated_text", "").strip()
                
                # If we get good content, return it
                if content and len(content) > 50:  # More flexible check
                    return content
            
        # If API fails or gives poor response, use fallback
        print(f"🔍 DEBUG: API failed or poor response, using fallback")
        print(f"🔍 DEBUG: Status code: {response.status_code}")
        return generate_fallback_questions(tech_stack)
        
    except Exception as e:
        print(f"🔍 DEBUG: API error: {str(e)}")
        print(f"🔍 DEBUG: Using fallback questions for {tech_stack}")
        return generate_fallback_questions(tech_stack)