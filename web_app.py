from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import json
from datetime import datetime
from database import restaurant_database

app = Flask(__name__)

client = genai.Client(api_key="API KEY")
db_string = json.dumps(restaurant_database, indent=2)

system_prompt = f"""
You are an expert UF campus dining assistant chatbot.
Your job is to answer user questions using ONLY the provided restaurant database below.
Do not assume or invent information not found in the database. If a match isn't found, state that politely.

RESTAURANT DATABASE:
{db_string}
"""

chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.0
    )
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask-gemini', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    user_lat = data.get('latitude')
    user_lon = data.get('longitude')
    
    live_time = datetime.now().strftime("%A, %I:%M %p")
    zone_description = f"at coordinates Latitude {user_lat}, Longitude {user_lon} near the UF campus"
    
    user_message = f"[System Note: The current live time is {live_time}] [User Location: {zone_description}]. Using ONLY the restaurant database, find the 3 closest open dining spots to this location and give a brief recommendation for each."
    
    try:
        response = chat.send_message(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error communicating with AI: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
