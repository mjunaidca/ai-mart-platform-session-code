from openai import OpenAI
from app import settings

client : OpenAI = OpenAI(api_key=str(settings.OPENAI_API_KEY))

def chat_completion(prompt : str )-> str:
    
 response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
# print(response)
#  print(response.choices[0].message.content)
 return response.choices[0].message.content


