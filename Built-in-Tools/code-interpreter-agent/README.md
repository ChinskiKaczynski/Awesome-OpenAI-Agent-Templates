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

| Mode | Description |
|------|-------------|
| `auto` | Automatic container management (recommended) |
| `explicit` | Create a container via the Containers API and pass its ID as `container` |

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

Code Interpreter-generated files are referenced by `container_file_citation` annotations on assistant messages (not by `code_interpreter_output` items). This example lists their IDs:

```python
for item in response.output:
    if item.type != "message":
        continue
    for part in item.content:
        if part.type != "output_text":
            continue
        for annotation in part.annotations:
            if annotation.type == "container_file_citation":
                print(f"Generated: {annotation.filename} (container: {annotation.container_id}, file: {annotation.file_id})")
```

To download the file bytes, use the [Containers file content API](https://developers.openai.com/api/docs/guides/tools-code-interpreter#work-with-files) while the container is active; the snippet above only prints file metadata. Containers expire after 20 minutes of inactivity.
