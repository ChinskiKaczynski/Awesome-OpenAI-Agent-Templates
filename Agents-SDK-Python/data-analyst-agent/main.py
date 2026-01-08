"""
Data Analyst Agent
An AI agent that analyzes data, generates insights, and creates reports.

Uses the Responses API with code_interpreter for calculations.
"""
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


# Sample dataset for demonstration
SAMPLE_DATA = """
Month,Revenue,Customers,Marketing_Spend,Churn_Rate
Jan,45000,120,5000,0.05
Feb,48000,135,5500,0.04
Mar,52000,150,6000,0.03
Apr,55000,165,6500,0.04
May,58000,180,7000,0.03
Jun,62000,200,7500,0.02
Jul,60000,195,7000,0.03
Aug,65000,220,8000,0.02
Sep,70000,240,8500,0.02
Oct,75000,260,9000,0.02
Nov,82000,290,10000,0.01
Dec,95000,350,12000,0.01
"""


class DataAnalystAgent:
    """Agent that analyzes data and generates insights."""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
    
    def analyze(self, data: str, question: str) -> str:
        """Analyze data and answer the question."""
        print(f"📊 Analyzing data...")
        print(f"❓ Question: {question}\n")
        
        response = client.responses.create(
            model=self.model,
            input=f"""You are a data analyst. Analyze this data and answer the question.

DATA (CSV format):
{data}

QUESTION: {question}

Instructions:
1. Use the code interpreter to load and analyze the data
2. Perform relevant calculations
3. Generate clear insights
4. Provide actionable recommendations

Format your response with:
- Key Metrics (numbers and percentages)
- Insights (what the data shows)
- Recommendations (what to do)

Use markdown formatting.""",
            tools=[
                {
                    "type": "code_interpreter",
                    "container": {"type": "auto"}
                }
            ]
        )
        
        return response.output_text
    
    def quick_stats(self, data: str) -> str:
        """Generate quick statistical summary."""
        print("📈 Generating quick stats...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Analyze this CSV data and provide:
1. Basic statistics for each numeric column (min, max, mean, median)
2. Total and averages
3. Any notable patterns

DATA:
{data}

Use code interpreter for accurate calculations. Format as a clear table.""",
            tools=[
                {
                    "type": "code_interpreter",
                    "container": {"type": "auto"}
                }
            ]
        )
        
        return response.output_text
    
    def trend_analysis(self, data: str) -> str:
        """Identify trends in the data."""
        print("📉 Analyzing trends...")
        
        response = client.responses.create(
            model=self.model,
            input=f"""Analyze trends in this time series data:

{data}

Calculate and report:
1. Overall trend (increasing/decreasing/stable)
2. Growth rates (period over period)
3. Seasonality patterns if any
4. Correlation between variables

Use code interpreter for calculations. Provide specific numbers.""",
            tools=[
                {
                    "type": "code_interpreter",
                    "container": {"type": "auto"}
                }
            ]
        )
        
        return response.output_text


def main():
    """Demo the data analyst agent."""
    agent = DataAnalystAgent()
    
    print("="*50)
    print("📊 DATA ANALYST AGENT DEMO")
    print("="*50)
    print("\nSample Data:")
    print(SAMPLE_DATA)
    print("="*50)
    
    # Analysis 1: Quick Stats
    print("\n\n--- QUICK STATS ---\n")
    stats = agent.quick_stats(SAMPLE_DATA)
    print(stats)
    
    # Analysis 2: Specific Question
    print("\n\n--- SPECIFIC ANALYSIS ---\n")
    analysis = agent.analyze(
        SAMPLE_DATA,
        "What's the relationship between marketing spend and revenue? "
        "Is the marketing investment paying off?"
    )
    print(analysis)
    
    # Analysis 3: Trend Analysis
    print("\n\n--- TREND ANALYSIS ---\n")
    trends = agent.trend_analysis(SAMPLE_DATA)
    print(trends)


if __name__ == "__main__":
    main()
