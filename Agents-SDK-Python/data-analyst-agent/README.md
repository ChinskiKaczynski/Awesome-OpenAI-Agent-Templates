# Data Analyst Agent

An AI agent that analyzes data, generates insights, and creates visualizations.

## Features

- 📊 **Data Analysis**: Process and analyze datasets
- 📈 **Insights Generation**: Identify trends and patterns
- 🧮 **Calculations**: Statistical analysis and metrics
- 📝 **Report Generation**: Create summary reports
- 🐍 **Code Execution**: Uses code interpreter for calculations

## Usage

```bash
pip install -r requirements.txt
python main.py
```

## Example Queries

```
"Analyze this sales data and identify top-performing products"
"Calculate month-over-month growth rates"
"Find correlations between marketing spend and revenue"
"Generate a summary of key metrics"
```

## How It Works

```
Data + Question
      ↓
┌──────────────┐
│  Understand  │ ← Parse question and data
└──────┬───────┘
       ↓
┌──────────────┐
│   Analyze    │ ← Run calculations (code interpreter)
└──────┬───────┘
       ↓
┌──────────────┐
│  Interpret   │ ← Generate insights
└──────┬───────┘
       ↓
   Report + Charts
```

## Output Example

```markdown
## Analysis Summary

### Key Metrics
- Total Revenue: $1.2M
- Growth Rate: 15% MoM
- Top Product: Widget Pro (35% of sales)

### Insights
1. Weekend sales 40% higher than weekdays
2. Q4 shows seasonal spike
3. Customer retention improving

### Recommendations
- Increase weekend marketing
- Prepare inventory for Q4
```
