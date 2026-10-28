
from ollama import chat

from tools import tools, run_tool


# -------------------------
# Configuration
# -------------------------

MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are a helpful local AI assistant.

You can calculate, search the web, and save Markdown documents
to the user's Obsidian vault.

When the user asks you to create, write, or save a document,
instruction manual, research report, or guide:

1. You MUST use the write_markdown tool.
2. Generate the complete document in Markdown.
3. Pass the document title and complete content to the tool.
4. Wait for the tool result before responding.
5. If saving succeeds, confirm the filename and location.
6. If saving fails, explain the error.

Never respond with only the document text when the user
has explicitly asked you to save it.

For instruction manuals:
- Use clear headings and numbered steps.
- Include prerequisites, examples and troubleshooting where useful.
- Use code blocks for commands and code.

For research reports:
- Organise findings into logical sections.
- Include a summary and conclusions.
- Include source titles and URLs returned by web search.
- Distinguish facts from assumptions and uncertainty.
- Never invent sources or claim to have verified something you have not.

Use clean, readable Markdown.
Use tables when they improve clarity.

Only save documents when the user asks you to create or save one.
When a document is saved, report the result to the user.
"""


# -------------------------
# Conversation memory
# -------------------------

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# -------------------------
# Main agent loop
# -------------------------

def main():
    print(f"AI agent started using {MODEL}.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        print("\n[Waiting for your question...]")
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Agent stopped.")
            break

        if not question:
            continue

        messages.append({
            "role": "user",
            "content": question
        })

        print("[Processing question...]")

        try:
            response = chat(
                model=MODEL,
                messages=messages,
                tools=tools
            )

            # Execute requested tools until Qwen finishes.
            while response.message.tool_calls:
                messages.append(response.message)

                for tool_call in response.message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    print(f"\n[Using tool: {tool_name}]")

                    result = run_tool(tool_name, arguments)

                    messages.append({
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(result)
                    })

                response = chat(
                    model=MODEL,
                    messages=messages,
                    tools=tools
                )

            answer = response.message.content or ""

            messages.append({
                "role": "assistant",
                "content": answer
            })

            print("\nAI:")
            print(answer)

        except Exception as e:
            print(f"\nAgent error: {e}")


if __name__ == "__main__":
    main()
