# Code Interpreter Agent

Sandboxed Python code execution using the `code_interpreter` built-in tool.

## Python

```bash
cd python
pip install -r requirements.txt
python main.py
```

## TypeScript

```bash
cd typescript
npm install
npx tsx main.ts
```

## What it does

1. Sends a request with `code_interpreter` tool enabled
2. Model writes and executes Python code in a secure sandbox
3. Returns results, including charts and generated files

## Example Use Cases

- Mathematical calculations
- Data analysis and visualization
- File format conversions
- CSV/JSON processing
- Chart generation

## Container Types

| Type | Description |
|------|-------------|
| `auto` | Automatic container management (recommended) |
| `reuse` | Reuse existing container for session |

## Expected Output

```
🧮 Query: Calculate the first 20 Fibonacci numbers and plot them
🔧 Running code interpreter...

🤖 Answer: Here are the first 20 Fibonacci numbers: [1, 1, 2, 3, 5, 8, 13, 21, ...]
📊 Generated chart: fibonacci_plot.png

💻 Code executed:
    def fibonacci(n):
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib
    ...
```

## Advanced: Accessing Generated Files

The code interpreter can generate files (charts, CSVs, etc.) that you can download:

```python
for output in response.output:
    if output.type == "code_interpreter_output":
        for file in output.files:
            print(f"Generated: {file.name}")
```
