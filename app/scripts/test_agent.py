from app.agent.agent_handler import run_agent

def test_agent():
    # Example input that would trigger a tool call
    print("Running agent test with input: 'Is cust_001 eligible for a rs 5000 loan?'")
    user_input = "Is cust_001 eligible for a 5000 rupees loan?"

    response = run_agent(user_input)

    print("Agent Response:", response)

if __name__ == "__main__":
    test_agent()