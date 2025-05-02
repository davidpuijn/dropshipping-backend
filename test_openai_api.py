import os
import openai
from dotenv import load_dotenv

# Laad .env bestand
load_dotenv()

# Haal key op uit omgevingsvariabelen
openai.api_key = os.getenv("OPENAI_API_KEY")

# Testvraag aan OpenAI
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Je bent een behulpzame assistent."},
            {"role": "user", "content": "Test of mijn API key werkt aub."}
        ]
    )
    print("✅ Verbinding gelukt! Antwoord van OpenAI:")
    print(response['choices'][0]['message']['content'])

except Exception as e:
    print("❌ Er ging iets mis met je API key:")
    print(e)
