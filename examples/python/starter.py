from agents import Agent, Runner

# Ensure OPENAI_API_KEY is set in your environment.
agent = Agent(name="Assistant", instructions="You are helpful and concise.")
if __name__ == "__main__":
    print(Runner.run_sync(agent, "Give me 3 unit testing tips.").final_output)
