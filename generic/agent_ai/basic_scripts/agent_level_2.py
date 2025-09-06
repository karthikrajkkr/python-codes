import os
import random
from openai import OpenAI
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculator_tool(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

def agent_decide(task):
    # Ask GPT to include reasoning in its response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI agent. You can either answer directly or call a tool. First explain your reasoning step by step, then give your action in the format: 'tool: <tool_name> <input>' or 'answer: <your_text>'. Whenever the task involves math, do not solve it yourself. Instead, output in the format: 'tool: <tool_name> <input>'"},
            {"role": "user", "content": f"Task: {task}"}
        ]
    )
    # Full AI message content
    pprint(response)
    full_message = response.choices[0].message.content.strip()
    return full_message

def agent_act(decision):
    print(f"AI Iteration:\n{decision}\n")  # show reasoning + decision

    # Extract action from last line (assumes last line contains tool/answer)
    last_line = decision.strip().splitlines()[-1]

    if last_line.startswith("tool:"):
        _, tool_name, expr = last_line.split(" ", 2)
        if tool_name == "calculator":
            result = calculator_tool(expr)
            print(f"Calculator result: {result}")
    elif last_line.startswith("answer:"):
        print(f"Agent answer: {last_line[7:]}")
    else:
        print(f"Agent unclear: {last_line}")

# --- Example tasks ---
tasks = ["What is 12 * 8?", "Say hello", "I am struggling with a calculation.output of 67*1-6"]

for t in tasks:
    decision = agent_decide(t)
    agent_act(decision)
    print("---")
