# Personal AI Assistant Agent

A modular, extensible AI agent built with Python and the Google Gemini API. Designed using SOLID principles and
Gang of Four (GoF) design patterns including Strategy, Factory/Registry, and
the ReAct (Reason → Act → Observe) agent loop.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [Tools](#tools)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Error Handling](#error-handling)

---

## Overview

This project implements an adaptive AI agent that:

- Maintains conversation history across a session
- Reasons about user requests using the Gemini LLM
- Autonomously decides when to use external tools via function calling
- Handles errors gracefully without crashing
- Follows the ReAct (Reason → Act → Observe) pattern

---

## Architecture

The system is separated into four core components following the Single Responsibility Principle:

```
User (CLI)
    ↓
Agent  ──→  MemoryManager  (stores conversation history)
    ↓
Gemini API  (reasoning and decision making)
    ↓
ToolRegistry  (Factory/Registry pattern)
    ↓
BaseTool  (Strategy pattern interface)
    ↓
Concrete Tools  (Calculator, Weather, Time, Translation, FileReader)
```

### ReAct Loop

```
1. Receive user input
2. Send full conversation history to Gemini
3. If Gemini requests a tool → execute it → send result back
4. Repeat until Gemini produces a final text answer
5. Save answer to memory and display to user
```

---

## Design Patterns

### Strategy Pattern
`BaseTool` defines an abstract interface. Every tool implements `execute()` and `get_declaration()`.
Tools are interchangeable and selected dynamically at runtime based on Gemini's decision.

### Factory / Registry Pattern
`ToolRegistry` manages all tool instances in a dictionary mapped by name.
The Agent never needs to know tool details — it simply calls `registry.execute(tool_name, args)`. 
Adding a new tool requires zero changes to the Agent class.

### SOLID Principles Applied

| Principle | Implementation |
|---|---|
| Single Responsibility | Each class has one job — Agent orchestrates, MemoryManager stores, ToolRegistry manages tools |
| Open/Closed | New tools can be added without modifying Agent or ToolRegistry core logic |
| Liskov Substitution | All tools are interchangeable through the BaseTool interface |
| Interface Segregation | BaseTool defines only what every tool needs |
| Dependency Inversion | Agent depends on abstractions (BaseTool), not concrete tool implementations |

---

## Project Structure

```
Agent/
├── .env                    ← API key (never commit this)
├── main.py                 ← CLI entry point
├── agent.py                ← Agent class with ReAct loop
├── memory.py               ← MemoryManager class
├── tool_registry.py        ← ToolRegistry (Factory pattern)
└── tools/
    ├── __init__.py
    ├── base_tool.py        ← Abstract BaseTool (Strategy pattern)
    ├── calculator.py       ← Safe math expression evaluator
    ├── weather.py          ← Real-time weather via wttr.in
    ├── time_tool.py        ← Current date and time
    ├── translation.py      ← Language translation (custom tool 1)
    └── file_reader.py      ← Local .txt file reader (custom tool 2)
```

---

## Tools

| Tool | Type | API Used | Description |
|---|---|---|---|
| Calculator | Built-in | Python `ast` module | Safely evaluates math expressions |
| Weather | External | wttr.in (free, no key) | Gets current weather for any city |
| Current Time | Built-in | Python `datetime` | Returns current date and time |
| Translation | Custom | MyMemory API (free) | Translates text between languages |
| File Reader | Custom | Local filesystem | Reads contents of .txt files |

---

## Requirements

- Python 3.11+
- Google Gemini API key (free from https://aistudio.google.com)
- Internet connection (for Gemini, weather, and translation)

### Python Packages

```
google-genai
requests
python-dotenv
```

---

## Installation

### 1 — Clone the repository

```bash
git clone https://github.com/yourusername/ai-personal-assistant.git
cd ai-personal-assistant/Agent
```

### 2 — Create and activate virtual environment

```bash
# Create venv with Python 3.11
py -3.11 -m venv venv

# Activate (Windows CMD)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3 — Install dependencies

```bash
pip install google-genai requests python-dotenv
```

---

## Configuration

### 1 — Get a Gemini API key

1. Go to https://aistudio.google.com
2. Click **Get API key**
3. Click **Create API key**
4. Copy the key

### 2 — Create a .env file

Create a file named `.env` in the `Agent` folder:

```
GEMINI_API_KEY=your_actual_key_here
```

> Never share or commit your `.env` file. It is already in `.gitignore`.

---

## Usage

### Start the assistant

```bash
python main.py
```

### Example interactions

```
You: What is 15% of 340?
Assistant: 15% of 340 is 51.

You: What is the weather in Riga?
Assistant: Riga, Latvia: 12°C, Partly cloudy

You: What time is it?
Assistant: Current date: Saturday, 21 March 2026 | Time: 14:32:10

You: Translate hello world to French
Assistant: Original (en): hello world
           Translated (fr): bonjour le monde

You: Read my notes.txt file
Assistant: Contents of 'notes.txt': ...

You: history
[Memory] 10 turns in conversation history.

You: quit
Assistant: Goodbye! Have a great day!
```

---

## Testing

### Test 1 — Multiple tools in one request
```
What time is it and what is the weather in Riga?
Calculate 15% of 850 and tell me the weather in London
```

### Test 2 — Failure scenarios
```
What is the weather in Xyzabc123?
Calculate the weather divided by banana
What is 100 divided by 0?
Read my fakefile.txt
```

### Test 3 — Memory verification
```
My name is John and I study Computer Science
(later) What is my name?
(later) What subject am I studying?
```

### Test 4 — Continued functioning after errors
After any error response, type a normal question — the agent should respond normally, proving the architecture is robust.

---

## Error Handling

The architecture handles errors at multiple levels:

| Error Type | Handled By | Behaviour |
|---|---|---|
| Unknown tool name | ToolRegistry | Returns error message, agent continues |
| Invalid tool arguments | Tool `execute()` method | Returns descriptive error, no crash |
| API rate limit | Agent try/except | Returns error message, loop continues |
| File not found | FileReaderTool | Returns friendly message |
| Invalid math expression | CalculatorTool | Returns descriptive error |
| No internet connection | WeatherTool / TranslationTool | Returns timeout message |
| Missing API key | Agent `__init__` | Raises clear EnvironmentError on startup |

---

## Author
Mapalo Chifota
Built with Python 3.11 and the Google Gemini API.
