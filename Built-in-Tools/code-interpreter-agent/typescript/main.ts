/**
 * Code Interpreter Agent
 * Sandboxed Python code execution using the code_interpreter built-in tool.
 */
import OpenAI from "openai";

const openai = new OpenAI();

async function runCodeInterpreter(query: string): Promise<string> {
    console.log(`🧮 Query: ${query}`);
    console.log("🔧 Running code interpreter...");

    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: query,
        tools: [
            {
                type: "code_interpreter",
                container: { type: "auto" },
            },
        ],
    });

    // Check for code interpreter outputs
    for (const output of response.output) {
        if (output.type === "code_interpreter_call") {
            console.log(`\n💻 Code executed:\n${output.code.slice(0, 200)}...`);
        }
    }

    return response.output_text;
}

async function main() {
    const tasks = [
        "Calculate the factorial of 20 and verify it's correct",
        "Generate a list of the first 15 prime numbers",
        "Calculate the compound interest for $1000 at 5% for 10 years",
    ];

    for (const task of tasks) {
        const answer = await runCodeInterpreter(task);
        console.log(`🤖 Answer: ${answer}\n`);
        console.log("-".repeat(50) + "\n");
    }
}

main();
