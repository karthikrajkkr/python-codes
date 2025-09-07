# This is level 2 where you are hard coding the input to the function/tool, and AI itself couldn't identify and call it.
# This is almost close to level 1. Only LLM.

from openai_module import generate_text_basic
from tools import get_weather

current_weather = get_weather("Montreal")

prompt = f"Do I need to take an Umbrella in Montreal tomorrow if it's {current_weather}?"

response = generate_text_basic(prompt, model="gpt-4")

print(response)