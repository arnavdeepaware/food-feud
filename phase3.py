import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

history = []
chat_session = model.start_chat(history=history)

PROMPT = "Based on these top restuarants in the United States of the Cuisine. Recommend me some unique and cool dishes that I can try to make at home. At the end take all restuarants into consideration and give me a list of ingredients I need. The output should have 2 things: all dishes and all ingredients"
response = chat_session.send_message(PROMPT)
model_response = response.text
response = json.loads(model_response)