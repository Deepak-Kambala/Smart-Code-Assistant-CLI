#!/usr/bin/env python3
import subprocess
from pathlib import Path
import sys
import typer

app = typer.Typer()

# Ensure UTF-8 encoding for Windows terminals
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def generate_debug_report(file_path: Path, model_name: str = "llama3.2:1b") -> str | None:
    """
    Generate a structured debug report for the given code file using Ollama.
    """

    try:
        code_content = file_path.read_text(encoding="utf-8")

        prompt = f"""You are a senior software engineer and debugging expert.

Carefully analyze the following code.

Your tasks:

1. Detect syntax errors.
2. Detect logical errors.
3. Detect runtime errors.
4. Identify bad practices or inefficiencies.
5. Clearly explain each issue.
6. Provide step-by-step solutions.
7. Provide a fully corrected version of the entire code at the end.

Format your response EXACTLY like this:

=== ERRORS FOUND ===
(List all issues clearly)

=== SOLUTIONS ===
(Explain how to fix them)

=== CORRECTED CODE ===
(Provide full corrected code)

Here is the code to debug:

{code_content}
"""

        typer.echo(f"Debugging {file_path} using model '{model_name}'...")

        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(input=prompt.encode("utf-8"))

        stdout = stdout.decode("utf-8", errors="replace")
        stderr = stderr.decode("utf-8", errors="replace")

        if process.returncode != 0:
            typer.secho(f"\n❌ Error running Ollama:\n{stderr}", fg=typer.colors.RED)
            return None

        return stdout

    except Exception as e:
        typer.secho(f"\n❌ An unexpected error occurred: {str(e)}", fg=typer.colors.RED)
        return None


def save_debug_report(file_path: Path, report: str) -> Path:
    """
    Save the debug report to a text file.
    """
    output_file = file_path.with_stem(file_path.stem + "_debug").with_suffix(".txt")
    output_file.write_text(report, encoding="utf-8")

    typer.secho(f"\n Debug report saved to: {output_file}", fg=typer.colors.GREEN)
    return output_file


@app.command()
def debug(
    file: Path = typer.Argument(..., exists=True, readable=True, help="The code file to debug."),
    model: str = typer.Option("llama3.2:1b", help="Ollama model to use.")
):
    """
    Please review and debug the following code.

If it contains any syntax errors, logical mistakes, runtime issues, or potential bugs, identify and explain them clearly.

For each issue you find:
- Explain why it is a problem.
- Provide a clear solution.
- Suggest improvements if applicable.

After identifying and explaining all issues, provide a fully corrected version of the entire code.

Then briefly describe the code’s purpose, main functions, and overall structure.

Here is the code:

{code_content}
    """

    report = generate_debug_report(file, model)

    if report:
        save_debug_report(file, report)
    else:
        typer.secho("⚠ Debugging failed.", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    app()
