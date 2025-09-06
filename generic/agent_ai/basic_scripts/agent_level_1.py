import os
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

environment_states = ["food", "enemy", "friend", "nothing"]

for _ in range(3):
    env = random.choice(environment_states)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a simple reflex agent. You must reply with one action only: eat, run, greet, explore, or wait."},
            {"role": "user", "content": f"Environment: {env}"}
        ]
    )

    action = response.choices[0].message.content.strip()
    print(f"Environment: {env} → Agent action: {action}")

