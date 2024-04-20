from pydantic_settings import BaseSettings
from pydantic import BaseModel, RootModel

from rich.console import Console
from groq import Groq

models = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "llama2-70b-4096",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

MODEL = models[0]
MAX_TOKENS = 50


class Settings(BaseSettings):
    GROQ_API_KEY: str


class Message(BaseModel):
    role: str
    content: str


class Conversation(RootModel):
    root: list[Message]

    def model_dump(self, *args, **kwargs):
        return [message.model_dump(*args, **kwargs) for message in self.root]

    def add(self, role: str, content: str):
        self.root.append(Message(role=role, content=content))

    def clear(self):
        self.root = [m for m in self.root if m.role == "system"]


def create_client(settings: Settings = Settings()):
    return Groq(api_key=settings.GROQ_API_KEY)


def generate_response(client: Groq, convo: Conversation, console: Console):
    completion = client.chat.completions.create(
        model=MODEL, messages=convo.model_dump(), max_tokens=MAX_TOKENS, stream=True
    )

    console.print("[bold red]>[/bold red] ", end="")
    response = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            if content:
                console.print(content, end="")
                response += content

    console.print("\n")

    convo.add(role="assistant", content=response)


def print_commands(console: Console):
    console.print("[bold cyan]Commands:[/bold cyan]")
    console.print("[cyan]!clear[/cyan] - Clear the console")
    console.print("[cyan]!exit[/cyan] - Exit the program")
    console.print("[cyan]!model[/cyan] - Change the active model")
    console.print("[cyan]!max_tokens[/cyan] - Change the max tokens")
    console.print("[cyan]!commands[/cyan] - Print this list of commands")
    console.print("\n")


def main():
    global MODEL, MAX_TOKENS

    console = Console()
    console.print("Welcome to Groq Chat!", style="bold red")
    console.print(
        "Type your message and press Enter to chat with the Groq API.",
        style="bold green",
    )
    console.print("[cyan]Active model: {}[/cyan]".format(MODEL))
    print_commands(console)

    convo = Conversation(
        [
            Message(role="system", content="You are a helpful assistant."),
        ]
    )

    client = create_client()

    try:
        while True:
            user_message = console.input("[bold green]>[/bold green] ").strip()

            if user_message.startswith("!"):
                if user_message == "!clear":
                    console.clear()
                    continue

                if user_message == "!clear_history":
                    convo.root.clear()
                    continue

                elif user_message.startswith("!model"):
                    _, *args = user_message.split(" ")
                    if args:
                        MODEL = args[0]
                        console.print(f"[cyan]Active model: {MODEL}[/cyan]")
                    else:
                        console.print(
                            f"> No model specified. Select one of {models}",
                            style="bold red",
                        )
                    continue

                elif user_message.startswith("!max_tokens"):
                    _, *args = user_message.split(" ")
                    if args:
                        MAX_TOKENS = int(args[0])
                        console.print(f"[cyan]Max tokens: {MAX_TOKENS}[/cyan]")
                    continue

                elif user_message.startswith("!commands"):
                    print_commands(console)
                    continue

                elif user_message == "!exit":
                    break

                else:
                    console.print("> Unknown command", style="bold red")
                    continue
            elif user_message == "":
                continue
            else:
                convo.add(role="user", content=user_message.strip())
                generate_response(client, convo, console)

    except (EOFError, KeyboardInterrupt) as _:
        console.print("\nGoodbye!", style="bold red")


if __name__ == "__main__":
    main()
