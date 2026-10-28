## What I'm trying to build

I'm currently learning about AI agents and how they actually work by building my own from scratch.

The main goal is to understand the different parts that make up an AI agent rather than just using an existing agent platform.

I want to gradually build it up so that it can:

- Understand a goal
- Decide what actions it needs to take
- Choose and use different tools
- Search for information
- Read and write files
- Analyse information
- Complete tasks without me having to tell it every individual step

> 💗 **Main goal:** Learn how AI agents actually work by building one myself, starting simple and adding functionality as I understand each part.

---

## What is an AI agent?

A normal AI conversation is:

```text
Question > AI > Answer
```

An AI agent can be given a goal and tools, allowing it to take actions itself.

For example:

```text
Goal
 V
AI decides what it needs to do
 V
Uses a tool
 V
Looks at the result
 V
Decides what to do next
 V
Uses another tool
 V
Final result
```

The important difference isn't that there's more steps.

The main difference is that it can take further actions rather than only giving me an answer.

For example, an agent could have access to tools such as:

```text
Search the web
Read files
Write files
Run Python
Calculate information
Analyse data
```

I could then give it a goal and allow it to decide which tools it needs to use.

---

## Normal AI vs an AI agent

A simple AI program might look like:

```text
Me
 V
Question
 V
AI model
 V
Answer
```

The AI agent I'm trying to build will eventually look more like:

```text
                 Goal
                  V
             ___________
             |   AI    |
             |_________|
                  V
          What should I do?
                  V
       _______________________
       |          |          |
       V          V          V
    Search      Python      Files
       |          |          |
       V          V          V
       _______________________
                  V
             Check result
                  V
          What should I do next?
                  V
                 ...
                  V
               Result
```

This repeated decision > action > result > decision cycle is what I'm interested in understanding and what makes it agentic.

---

## My first setup

I'm starting with a local AI setup so I can experiment without needing to pay for an AI API.

The basic setup is:

```text
My PC
 |
 L__ Python
 |
 L__ AI Agent
 |
 L__ Ollama
       |
       L_ Local AI model
```

I'm using Ollama to run an AI model locally on my computer.

This allows my Python program to communicate with the model running on my own computer rather than sending each request to a paid cloud AI API.

> 🌸 **Why I'm doing it this way:** I want to understand what's happening underneath an AI agent instead of just using a platform where most of the process is hidden from me.

---

## Project location

I'm keeping the project in OneDrive so my code, notes and research can be backed up and synchronised.

The project will look roughly like:

```
OneDrive
L_ -AI-Agent
   L_ - agent.py
   L_ - research notes
```

The Ollama models themselves don't need to be stored in OneDrive because they are large files and Ollama manages them separately.

So:

```
OneDrive
> Code + research + notes

Local PC
> Ollama + AI model
```

```
Your PC
|  
L __Python 3.14
|
L __Ollama
|     --AI model
|      
L __Python Ollama package
          v
   Can talk to Ollama
```


## Talking to the model

My first experiment was getting Python to send a question to the local Qwen model and print the response.

```
from ollama import chat

response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "Explain what an AI agent is in simple terms."
        }
    ]
)

print(response.message.content)
```

#### Response
```
An **AI agent** is like a computer program or system that can **sense its environment**, **think about what to do**, and **take actions** to achieve a specific goal-just like a person might. Here's a simple breakdown:

1. **Senses its environment**: It gathers information from its surroundings (like a robot seeing its world or a app checking your preferences).
2. **Decides what to do**: It uses rules, data, or learning to figure out the best action.
3. **Acts to achieve a goal**: It takes steps to reach its target, like a virtual assistant scheduling a meeting or a self-driving car avoiding obstacles.

**Examples**:
- A **smart thermostat** that adjusts your home's temperature based on weather.
- A **recommendation system** (like Netflix or Spotify) that suggests content you might like.
- A **chatbot** that answers your questions.

In short, an AI agent is a tool that *thinks* and *acts* to solve problems or meet goals, often improving over time by learning from experience. 🤖💡

It answered it but it took a few minutes the answer was quite long, and this version would not be able to remember any of my messages from previous interactions
``` 

The model successfully generated an answer explaining the basic idea of an AI agent.

But this program runs one question per program, this means if I wanted to ask a new question I would need to edit the python script. 

Every time I sent a request, it was starting a new conversation and every time it responded that was the end of the conversation.

The program was doing:

```
Question
   v
   AI
   v
Answer
```

## Making it interactive

The next step was to make the program behave more like a conversation.

I added a while loop so that I could repeatedly enter questions until I typed exit or quit.

```
from ollama import chat

while True:
    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        break

    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("\nAI:")
    print(response.message.content)
```

#### Response

```text

You: my name is lizzie

AI:
Hi Lizzie! 😊 How can I assist you today? Whether you need help with something specific or just want to chat, I'm here for you! What's on your mind?

You: whats my name

AI:
I don't have access to your name unless you've provided it in our conversation so far. If you'd like to share your name, I'd be happy to use it! How can I assist you today? 😊

You:
```

This made the program interactive, but it still didn't feel like a conversation.

Although it looked like a conversation to me, the AI wasn't actually receiving the previous messages in the next queries.

The program was actually doing:

Question 1 > AI > Answer

Question 2 > AI > Answer

Question 3 > AI > Answer

Each request was independent.

## Adding conversation history


To solve this, I needed to store the conversation and send that history back to the model with every new question.

I created a Python list called messages


```python
from ollama import chat

messages = []

while True:
    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        break

    messages.append({
        "role": "user",
        "content": question
    })

    response = chat(
        model="qwen3:8b",
        messages=messages
    )

    messages.append({
        "role": "assistant",
        "content": response.message.content
    })

    print("\nAI:")
    print(response.message.content)
```

Now every time I send a new question, the program sends the stored messages back to Qwen along with my new question. 


```
You: hi im lizzie

AI:
Hi Lizzie! 😊 How are you doing today? I'm here to chat, help, or just listen if you need anything. What's on your mind?

You: whats my name

AI:
Your name is Lizzie! 😊 How can I assist you today?
```

This works as a kind of short term memory, but as the conversation gets longer it takes more tokens for every next question.

Qwen is running locally on my CPU and generating its response token by token. I'm also repeatedly providing the entire conversation history as context. 

> ✨ **Potential next step:** Could I save just key bits of information in a dictionary, e.g. `[name:Lizzie, gender:female, topic: weather]`

## Giving the AI tools

Now that I had basic conversation and short-term memory working, I wanted to move towards something more agent-like.

The next step was giving the model access to tools.

The first tools I'm experimenting with are:
- Calculator
- Web search

The calculator allows the Python program to perform calculations rather than relying on the language model to generate the answer itself.

I'll be using duckduckgo for web search.

Instead of giving Qwen direct access to the internet my python script can call it as a tool

```
You: what is 7+2

AI:
The result of 7 + 2 is **9**.

You:
```


```
[Waiting for your question...]
You: who is the ceo of microsoft
[Processing question...]

[Using tool: web_search]

AI:
The current CEO of Microsoft is **Satya Nadella**. He has held this position since 2014 and is also the Chairman of the Board. Nadella has led Microsoft's transformation toward cloud computing and AI innovation.

[Waiting for your question...]
You:
```
> [!INFO]-
> I had to add some debug prints to check the order but I like them so I'll keep them in from now on!


To get this answer it took a total of around 70 seconds, I added a time function to check where the model was spending most of the time 

it gave me the following 

```text
[Waiting for your question...]

You: who is the ceo of microsoft
[Processing question...]
[Qwen response time: 32.61s]

[Using tool: web_search]
[Web search time: 2.53s]
[Qwen final response time: 40.28s]

AI:
The current CEO of Microsoft is **Satya Nadella**. He has held this position since January 2014, succeeding Steve Ballmer. Nadella is also the chairman of the Microsoft Board of Directors.

```

| Stage                       |       Time |
| --------------------------- | ---------: |
| Qwen decides what to do     | **32.61s** |
| Web search                  |  **2.53s** |
| Qwen reads result + answers | **40.28s** |
As its running locally on my device it indicates a hardware issue/bottleneck
Turns out I was using CPU rather than GPU

> [!INFO]+
> The hardware the AI is running on matters alot more than the version when it comes to speed


## Write to document tool

So far, my agent could answer questions, use a calculator and search the web. However, the answers were only being returned in the terminal. I wanted to give it another tool that would allow it to save useful information as Markdown documents directly into my Obsidian vault.

The idea was that I could ask my agent to write up something it had explained or create an instruction manual, and instead of having to copy and paste the answer into Obsidian myself, it would create the document for me.

This also meant that the agent could start helping me document the development of the project itself.

I decided to separate his into two different python scripts; using: `agent.py` to handle the conversation and to decide when a tool is needed, while `tools.py` contains the functions that actually perform the tasks.

The writer was set up to do the following:

- Check that the Obsidian vault path exists before trying to save anything.
- Create the `AI Generated` folder if it doesn't already exist.
- Clean up the document title so it can safely be used as a Windows filename.
- Make sure the document has a main heading.
- Save the document using UTF-8 encoding.
- Avoid overwriting an existing document by adding a number to the filename when necessary.

### Testing it through the agent

After connecting the tool, I wanted to test whether the agent could use it through a normal request. 

````
You: Create a short instruction manual explaining how to check my Python version on Windows, and save it to Obsidian.
[Processing question...]

AI:
Here's a concise instruction manual:

**How to Check Python Version on Windows**
1. Open Command Prompt (Win+R > cmd)
2. Type: `python --version` or `python -V`
3. Alternatively: `where python` then check file properties

**Save to Obsidian:**
1. Open Obsidian and create a new note
2. Add code block:
```cmd
python --version
python -V
```
3. Use Obsidian's "Insert Code Block" feature (</code>)

Would you like me to format this as a markdown file for direct import into Obsidian?

[Waiting for your question...]
````

At first, there was an issue with how the model handled the request. Even though the Markdown writer existed and worked when tested directly, the model could still respond to a request by writing the instructions or document content in the terminal instead of actually calling `write_markdown`.

To fix this, I needed to look at the `SYSTEM_PROMPT` in `agent.py`.

The system prompt gives the model its general instructions for how it should behave. Although the tool was available to it, simply making a tool available doesn't guarantee that the model will use it in the way I intended.

I therefore needed to make the instructions clearer about when the model should use the Markdown writer, so when I ask the agent to create or save a document, it should use the `write_markdown` tool rather than just returning the document content in the conversation.


### It worked!!!

After updating the system prompt, I tested the agent again by asking it to create a document.

This time, the agent successfully used `write_markdown` and created a file called `Checking Python Version on Windows.md`.

```
You: Create a short instruction manual explaining how to check my Python version on Windows, and save it to Obsidian.
[Processing question...]

[Using tool: write_markdown]

AI:
Your instruction manual has been saved successfully to Obsidian at the following path:
----------\AI_Notes\AI Generated\Checking Python Version on Windows.md`

Let me know if you'd like to create additional guides or need help with anything else! 🐍

[Waiting for your question...]
You:
```

Markdown document
```markdown
# Checking Python Version on Windows

## How to Check Your Python Version on Windows

### Prerequisites
- Python must be installed on your system
- Windows operating system

### Method 1: Using Command Prompt
1. Press `Win + R` to open the Run dialog
2. Type `cmd` and press Enter
3. In the Command Prompt, type:
   ```bash
   python --version
   ```
   or
   ```bash
   python -V
   ```
4. Press Enter. The version number will appear (e.g., `Python 3.11.4`).

### Method 2: Checking via Start Menu
1. Click the Start button
2. Look for Python in the list of installed programs
3. The version will be displayed in the program name (e.g., `Python 3.10`).

### Troubleshooting
- If `python` isn't recognized, add Python to your system PATH during installation.
- Ensure you're using the correct Python executable (sometimes multiple versions are installed).
```