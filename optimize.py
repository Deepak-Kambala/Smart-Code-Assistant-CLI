#!/usr/bin/env python3
import subprocess
from pathlib import Path
from typing import Optional
import typer

# Initialize Typer app
app = typer.Typer()


# ----------------------------------
# Core Ollama Runner
# ----------------------------------
def run_ollama(prompt: str, model_name: str) -> Optional[str]:
    """
    Run Ollama with the given prompt and return the output.
    """
    try:
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = process.communicate(input=prompt.encode("utf-8"))

        if process.returncode != 0:
            typer.echo(f"[ERROR] Ollama error:\n{stderr.decode()}", err=True)
            return None

        return stdout.decode("utf-8", errors="replace")

    except Exception as e:
        typer.echo(f"[EXCEPTION] {str(e)}", err=True)
        return None


# ----------------------------------
# Optimization Logic
# ----------------------------------
def generate_optimization(file_path: Path, model_name: str) -> Optional[str]:
    """
    Analyze and optimize the given code.
    """

    try:
        typer.echo(f"Reading file: {file_path}")
        code_content = file_path.read_text(encoding="utf-8")

        prompt = f"""You are a senior performance engineer and algorithm expert.

Analyze the following code strictly from an optimization perspective.

Your tasks:

1. Identify inefficiencies in time complexity.
2. Identify memory inefficiencies.
3. Suggest better algorithms if applicable.
4. Suggest better data structures.
5. Suggest more Pythonic or cleaner implementations.
6. Suggest design improvements if relevant.
7. Compare time and space complexity (before vs after).
8. Provide a fully optimized version of the code.

Do NOT explain basic functionality unless necessary.
Focus only on performance, scalability, and clean design.

Here is the code:

{code_content}
"""

        typer.echo(f"Optimizing using model: {model_name}...")
        return run_ollama(prompt, model_name)

    except Exception as e:
        typer.echo(f"[EXCEPTION] {str(e)}", err=True)
        return None


def save_output(file_path: Path, content: str) -> Path:
    """
    Save optimization output to file.
    """
    output_file = file_path.with_name(f"{file_path.stem}_optimized.txt")
    output_file.write_text(content, encoding="utf-8")

    typer.echo(f"[✓] Optimization saved to: {output_file}")
    return output_file


# ----------------------------------
# CLI Command
# ----------------------------------
@app.command()
def optimize(
    file: str = typer.Argument(..., help="The code file to optimize"),
    model: str = typer.Option("llama3.2:1b", help="Ollama model to use"),
):
    """
    Optimize a code file by suggesting better algorithms,
    data structures, and performance improvements.
    """

    resolved_path = Path(file).resolve()

    if not resolved_path.is_file():
        typer.echo(f"[ERROR] File not found: {resolved_path}", err=True)
        raise typer.Exit(1)

    optimization = generate_optimization(resolved_path, model)

    if optimization:
        save_output(resolved_path, optimization)


# ----------------------------------
# Entry Point
# ----------------------------------
if __name__ == "__main__":
    app()
