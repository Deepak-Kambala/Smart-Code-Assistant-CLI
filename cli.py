import typer
from smart_code_assistant.explainer import explain
from smart_code_assistant.test import generate 
from smart_code_assistant.debug import debug
from smart_code_assistant.optimize import optimize

app = typer.Typer()

app.command()(explain)
app.command(name="test")(generate)
app.command()(debug)
app.command()(optimize)

if __name__ == "__main__":
    app()
