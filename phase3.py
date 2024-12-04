import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Create the model
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
  system_instruction="You are a restuarant reviewer. You help people with recommeding restaurants, cuisines, foods and dishes. You also help them with cooking at home sharing new and exciting recipies and ingredients to try at home.",
)

history = []
print(os.getenv('CUISINE'))
msg = "Based on these top restuarants in the United States of the " + str({os.getenv('CUISINE')}) +" Cuisine. Recommend me some unique and cool dishes that I can try to make at home. At the end take all restuarants into consideration and give me a list of ingredients I need. The output should have 2 things: all dishes and all ingredients"


while True:
    try:
        user_input = msg

        chat_session = model.start_chat(
            history= history
        )

        response = chat_session.send_message(user_input)
        model_response = response.text

        res = json.loads(model_response)

        #print(model_response)
        #print(type(model_response))
        #print(res["ingredients"])

        for i in res["ingredients"]:
            print(i)
        break
    except KeyError:
        continue


'''
print("ingredients:")

for ingredient in res['ingredients']:
    print(ingredient)
    print()
'''
