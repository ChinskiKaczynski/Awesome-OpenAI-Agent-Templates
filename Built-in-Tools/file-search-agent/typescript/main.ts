/**
 * File Search Agent
 * Document search using the file_search built-in tool with vector stores.
 * 
 * Prerequisites:
 * 1. Create a vector store in OpenAI Dashboard
 * 2. Upload documents to the vector store
 * 3. Set VECTOR_STORE_ID environment variable
 */
import OpenAI from "openai";

const openai = new OpenAI();

const VECTOR_STORE_ID = process.env.VECTOR_STORE_ID || "vs_YOUR_VECTOR_STORE_ID";

async function searchDocuments(query: string): Promise<string> {
    console.log(`📚 Query: ${query}`);
    console.log(`🔍 Searching vector store ${VECTOR_STORE_ID.slice(0, 20)}...`);

    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: query,
        tools: [
            {
                type: "file_search",
                vector_store_ids: [VECTOR_STORE_ID],
            },
        ],
    });

    return response.output_text;
}

async function main() {
    if (VECTOR_STORE_ID === "vs_YOUR_VECTOR_STORE_ID") {
        console.log("⚠️  Please set VECTOR_STORE_ID environment variable");
        console.log("   Create a vector store at: https://platform.openai.com/storage");
        return;
    }

    const queries = [
        "What are the main topics covered in the documents?",
        "Summarize the key points from the documentation.",
    ];

    for (const query of queries) {
        const answer = await searchDocuments(query);
        console.log(`🤖 Answer: ${answer}\n`);
        console.log("-".repeat(50) + "\n");
    }
}

main();
