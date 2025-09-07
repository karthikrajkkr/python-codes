# This is level 4 where you need not to use openai modules, and related functions.
# Instead,we can use one module simplerLLM that has integration to all the LLMs such as Gemini,Anthropic, etc

from prompts import react_system_prompt
from tools import get_weather
from dotenv import load_dotenv

from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text

load_dotenv()

llm_instance = LLM.create(provider=LLMProvider.OPENAI,model_name="gpt-3.5-turbo")

#Available actions are:
available_actions = {
    "get_weather": get_weather
}

prompt = f"Do I need to take an Umbrella in Montreal tomorrow?"

# prompt = "what is gandhi"

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

    response = llm_instance.generate_response(messages=messages)

    print("Agent response:", response)

    json_function = extract_json_from_text(response)

    print(json_function)

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