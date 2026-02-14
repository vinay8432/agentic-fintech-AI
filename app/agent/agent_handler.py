from openai import OpenAI
import json
import os
from dotenv import load_dotenv 
from app.tools.loan_tools import get_customer_loan_eligibility

TOOLS = [
    {
        "type": "function",
        "name": "get_customer_loan_eligibility",
        "description": "Evaluate whether a customer is eligible for a loan under current policy.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Unique identifier of the customer"
                },
                "loan_amount": {
                    "type": "number",
                    "description": "Requested loan amount"
                }
            },
            "required": ["customer_id", "loan_amount"],
            "additionalProperties": False
        }
    }
]


load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


#i want to use the local model that i have running on my machine, so i will set the base url to localhost:8000
# client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
client = OpenAI()

def run_agent(user_input: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=user_input,
        tools=TOOLS
    )

    print("Agent raw response:", response)

    for output in response.output:

        if output.type == "function_call":

            tool_name = output.name
            arguments = output.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            if tool_name == "get_customer_loan_eligibility":

                customer_id = arguments.get("customer_id")
                loan_amount = arguments.get("loan_amount")

                tool_result = get_customer_loan_eligibility(
                    customer_id, loan_amount
                )

                print(f"Tool executed → {tool_result}")

                # ✅ Correct second call
                final_response = client.responses.create(
                    model="gpt-4.1-mini",  # SAME MODEL
                    previous_response_id=response.id,
                    input=[
                        {
                            "type": "function_call_output",
                            "call_id": output.call_id,
                            "output": json.dumps(tool_result)
                        }
                    ]
                )

                return final_response.output_text

    return response.output_text

