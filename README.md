# Smart Code Assistant CLI

## Short Description
Smart Code Assistant CLI helps beginners debug, optimize, explain, and generate tests for Python code instantly, powered by an offline **Ollama 3.21B** model. It keeps developers focused by providing AI-powered solutions directly in the project directory.

## Features
- **Code Debugger** – Automatically detects issues in your code and generates a text file with suggestions.
- **Code Optimizer** – Analyzes your code and suggests more efficient alternatives in a separate file.
- **Code Explainer** – Provides clear explanations of your code logic up to a specific point.
- **Test Generator** – Generates sample test cases to validate correctness and handle edge cases.
- **Offline Support** – Powered by Ollama 3.21B, works entirely offline without internet dependency.
- **Fast Execution** – Commands execute in 2–3 seconds (network optional) for instant feedback.

## How It Works
1. Execute a custom command (e.g., `debug`) in your terminal.
2. Your code is sent to the **Ollama LLM** for processing.
3. The generated output (debugged code, optimized version, explanation, or tests) is saved as a text file in your project folder.
4. No need to switch tools—stay focused and reduce attention residue.

## Supported Commands
| Command        | Description |
|----------------|-------------|
| `debug`        | Debugs your code and writes suggestions to a file. |
| `optimize`     | Suggests improvements for efficiency. |
| `explain`      | Explains your code logic clearly. |
| `generate-test`| Creates sample test cases for validation. |

## Tech Stack
- Python
- Ollama 3.21B LLM (offline)
- Windows PowerShell (custom CLI commands)
