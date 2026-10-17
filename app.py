from google import genai
from google.genai import types
from database import restaurant_database
import json

client = genai.Client(api_key="API KEY")


db_string = json.dumps(restaurant_database, indent=2)

system_prompt = f"""
You are an expert UF campus dining assistant chatbot.
Your job is to answer user questions using ONLY the provided restaurant database below.
Do not assume or invent information not found in the database. If a match isn't found, state that politely.

The current day and time is: current_time

Format every answer like this:
Start with a one-line intro that reacts to the user's request.

For each spot:

**{{emoji}} {{Name}}** · {{price}} · {{diet tag}}
{{One casual sentence on why it fits what they asked for: speed, budget, vibe, etc.}}
- 📍 {{Landmark-based location, short}}
- ⏰ {{Open status relative to now, e.g. "Open now till 2pm" / "Opens at 11am" / "Closed today, back Monday"}}
- ⚡ {{Speed + seating, short}}
- 🗺️ [Get directions]({{maps link}})

End with a one-line top pick or a follow-up question.

If unable to find a suitable spot based on the user's request, politely inform them that you can't generate any suitable recommendations and suggest alternatives if available.

Rules:
- Use 12-hour times (2pm, not 14:00).
- Only show today's open status, not the full weekly schedule.
- Max 3 spots unless the user asks for more.

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

if __name__ == "__main__":
    print("🐊 UF Campus Dining Chatbot is live! Type 'exit' or 'quit' to stop.\n")
    while True:
      try:
          user_input = input("You: ")
          if user_input.lower() in ["exit", "quit"]:
              print("Goodbye! Enjoy your meal on campus!")
              break
          if not user_input.strip():
              continue
          from datetime import datetime
          live_time = datetime.now().strftime("%A, %I:%M %p")
          injected_prompt = f"[System Note: The current live time is {live_time}] \nUser Question: {user_input}"
          response = chat.send_message(injected_prompt)
          print(f"\nGemini: {response.text}\n" + "-"*50)
      except KeyboardInterrupt:
          print("\nGoodbye!")
          break

