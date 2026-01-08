/**
 * Computer Use Agent
 * Browser and desktop automation using the computer_use_preview built-in tool.
 * 
 * ⚠️ Preview Feature: This API is in preview and may change.
 */
import OpenAI from "openai";

const openai = new OpenAI();

interface TaskResult {
    task: string;
    output: string;
    steps: Array<{ action: string }>;
}

async function executeTask(
    task: string,
    environment: "browser" | "computer" = "browser"
): Promise<TaskResult> {
    console.log(`🖥️  Task: ${task}`);
    console.log(`   Environment: ${environment}`);
    console.log("   Running...");

    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: `You are a computer use assistant. Complete this task:

Task: ${task}

Use the computer_use tool to:
1. Navigate to the appropriate website/application
2. Perform the necessary actions (click, type, scroll)
3. Extract and return the requested information

Be methodical and verify each step.`,
        tools: [
            {
                type: "computer_use_preview",
                display_width: 1024,
                display_height: 768,
                environment: environment,
            },
        ],
    });

    const result: TaskResult = {
        task: task,
        output: response.output_text,
        steps: [],
    };

    // Extract computer use steps
    for (const output of response.output) {
        if (output.type === "computer_call") {
            const step = {
                action: String(output.action),
            };
            result.steps.push(step);
            console.log(`   📸 Action: ${step.action}`);
        }
    }

    return result;
}

async function scrapePage(url: string, extract: string): Promise<string> {
    const task = `Go to ${url} and extract: ${extract}`;
    const result = await executeTask(task);
    return result.output;
}

async function main() {
    console.log("=".repeat(50));
    console.log("🖥️  COMPUTER USE AGENT DEMO");
    console.log("=".repeat(50));
    console.log("\n⚠️  Note: This is a preview feature");
    console.log("   Requires computer_use_preview access\n");

    // Demo 1: Simple scraping task
    console.log("\n--- Task 1: Information Extraction ---\n");
    const result1 = await executeTask(
        "Go to example.com and tell me what the main heading says"
    );
    console.log(`✅ Result: ${result1.output}`);

    // Demo 2: Search task
    console.log("\n--- Task 2: Search ---\n");
    const result2 = await executeTask(
        "Use a search engine to find the current weather in New York"
    );
    console.log(`✅ Result: ${result2.output}`);

    console.log("\n" + "=".repeat(50));
    console.log("Demo complete!");
}

main();
