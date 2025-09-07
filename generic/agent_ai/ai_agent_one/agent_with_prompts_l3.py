# This is level 3 where you instruct the LLM to take action based on user input by writing prompts and passing functions/tools to them.

from openai_module import generate_text_with_conversation
from prompts import react_system_prompt
from tools import get_weather
from json_helper import extract_json

#Available actions are:
available_actions = {
    "get_weather": get_weather
}

prompt = f"Do I need to take an Umbrella in Montreal tomorrow?"

# prompt = "what is CO2 chemical"

messages = [
    {"role": "system", "content": react_system_prompt},
    {"role": "user", "content": prompt},
]

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print(f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages, model="gpt-3.5-turbo")

    print("Agent response:", response)

    json_function = extract_json(response)

    if json_function:
        function_name = json_function[0]['function_name']
        function_parms = json_function[0]['function_parms']
        if function_name not in available_actions:
            raise Exception(f"Unknown action: {function_name}: {function_parms}")
        print(f" -- running {function_name} {function_parms}")
        action_function = available_actions[function_name]
        result = action_function(**function_parms)
        function_result_message = f"Action_Response: {result}"
        messages.append({"role": "user", "content": function_result_message})
    else:
        # ✅ handle direct answers too
        if response.strip().lower().startswith("answer:"):
            print(response)  # Final answer from LLM
        else:
            print("Agent ended with:", response)
        break