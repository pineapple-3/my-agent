## Local AI Agent
(First draft)

A personal project exploring how AI agents work by building one from scratch using Python, Ollama and a locally running language model.

The aim is to understand how an agent communicates with a model, uses tools, carries out tasks and eventually handles more complex workflows.

This project is still under development, and I'm using it to learn about agent architecture, tool calling, local AI and Python.

#### Current Features

The agent currently supports:

Local AI model: Communicates with Qwen3:8B through Ollama.

Calculator: Performs calculations using a restricted expression evaluator.

Web search: Searches the web for information using DuckDuckGo.(Search results can be incomplete or incorrect)

Markdown writer: Creates Markdown documents directly in an Obsidian vault. The writer checks the path, prepares the output folder, cleans filenames and checks to not overwrite any  existing documents with the same name.



Tool calling: Allows the model to request tools when they are useful for a task.

### How It Works

The project is split into two main Python files, agent.py and tool.py

agent.py - Handles the conversation with the model and manages tool calls.
tool.py - Contains the Python functions that perform the available tools.

The general workflow is:

I enter a request in the terminal
The agent sends the conversation to the local model through Ollama
The model responds or requests a tool
The agent runs the requested tool through tools.py
The result is returned to the model, which can continue the task and respond.


### Requirements

You need:
Python 3
Ollama
Qwen3:8B model
Internet connection for web searches
An Obsidian vault

The model runs locally through Ollama. The Python ollama package provides the connection between my code and Ollama; it does not install the model itself.


### Installation

##### 1.Clone the repository

```
git clone <repository-url>
cd my-agent
```
Replace <repository-url> with the URL of this GitHub repository.

##### 2.Create a virtual environment

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
##### 3.Install the Python dependencies

```
pip install -r requirements.txt
```
##### 4.Download the model

Install and open Ollama, then run:

```
ollama pull qwen3:8b
```
Make sure Ollama is running before starting the agent.

##### 5.Configure the Obsidian vault

The Markdown writer uses the OBSIDIAN_VAULT_PATH environment variable to identify the vault where generated documents should be saved.

For example, in Windows PowerShell:

```
$env:OBSIDIAN_VAULT_PATH = "C:\Users\YourName\Documents\MyVault"
```
Replace the example with the path to your own vault. The path should point to the vault root, not the AI Generated subfolder.

##### 6.Run the agent

```
python agent.py
```
You should then be able to interact with the agent through the terminal.

## About This Project

This is an early-stage project. my longer-term goal is to develop an agent that can plan and carry out more complex tasks, rather than only responding to individual requests.

I'm building this project to develop a deeper understanding of AI agents, Python, local language models and the systems that allow models to interact with external tools.

I'm documenting the development process as I go, including what works, what fails and what I learn along the way. (please see WorkinProgress-log.md for my thought process along he way!)



