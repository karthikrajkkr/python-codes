# This is level 1 where you are just interacting with openai like you do in ChatGPT.
# No agents are involved here.

from openai_module import generate_text_basic

prompt = "Top 10 countries with powerful militaries?"

response = generate_text_basic(prompt)

print(response)