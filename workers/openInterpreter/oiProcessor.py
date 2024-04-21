from groq import Groq
from interpreter import interpreter

from enum import Enum
import sys
import os


def initializeGroqClient():
    apiKey = os.environ.get("GROQ_API_KEY")
    groqClient = Groq(api_key=apiKey)
    return groqClient


def initializeOpenAIClient():
    apikey = os.environ.get("OPENAI_API_KEY")  # noqa: F841


def determineResult(resultString):
    # print(resultString)
    resultString = resultString.lower()
    if "no" in resultString:
        return True
    return False


class PromptController:
    PromptExpressingDeterminer = "You are an Insurance question detector, all you do is say yes or no if a question concerns insurance"

    def __init__(self, prompt):
        self.prompt = prompt
        self.groqClient = initializeGroqClient()

    def isOI(self):
        queryReturn = self.groqClient.chat.completions.create(
            messages=[
                {"role": "system", "content": self.PromptExpressingDeterminer},
                {"role": "user", "content": self.prompt},
            ],
            model="mixtral-8x7b-32768",
        )
        return determineResult(queryReturn.choices[0].message.content)


class OIProcessor:
    def __init__(self):
        interpreter.llm.api_key = os.environ.get("OPENAI_API_KEY")
        interpreter.verbose = False
        interpreter.conversation_history = True
        interpreter.auto_run = True

    def performWorkFlow(self, prompt):
        lowerPrompt = prompt.lower()
        if "email" in lowerPrompt or "email." in lowerPrompt or "email!" in lowerPrompt:
            lowerPrompt = self.emailWorkflow()
        elif (
            "message" in lowerPrompt
            or "message!" in lowerPrompt
            or "message." in lowerPrompt
        ):
            lowerPrompt = self.textMessageWorkflow()
        elif "setup text" in lowerPrompt:
            lowerPrompt = self.setUpMessagingWorkflow()
        else:
            pass
        fullMessage = (
            lowerPrompt
            + ". do this with the assumption that I use an Ubuntu laptop I give you consent to control my system's applications. Use google chrome for any web browsing."
        )
        self.communicateWithOpenInterpreter(fullMessage)

    def emailWorkflow(self):
        emailAddress = input("Please enter your email address: ")
        emailSubject = input("Please enter the subject of the email: ")
        emailMessage = input("Please enter your")
        return f"send an email to {emailAddress} with subject {emailSubject} and body {emailMessage}"

    def textMessageWorkflow(self):
        personToSendTo = input("who do you want to send the message to: ")
        messageToSend = input("What message do you want to send: ")
        return f"find the contacts.json file in my current directory, convert it to a dictionary, find the value for the key {personToSendTo} use this as a phone number and send them the message {messageToSend}"

    def setUpMessagingWorkflow(self):
        personName = input("What is the person's name")
        personNumber = input("What is the person's phone number")
        return f"in the contacts.json file in my current directory, convert it to a dictionary, add the key {personName} and give it value the key {personNumber}, and save this as the new contacts.json file"

    def communicateWithOpenInterpreter(self, fullprompt):
        interpreter.chat(fullprompt)
        condition = str(interpreter.messages[1].get("content"))
        if (
            "proceed" in condition.lower()
            or "now" in condition.lower()
            or "let's" in condition.lower()
        ):
            interpreter.chat("proceed")
        return condition

    # workflow for play, asks for medium, then goes to google, spotify or apple music


class Chubb_Processor:
    def __init__(self):
        self.apiKey = os.environ.get("OPENAI_API_KEY")


class Msg(str, Enum):
    PROMPT: str = "[PROMPT]"
    STOP: str = "[STOP]"
    READY: str = "[READY]"


def prompt_pipeline(prompt):
    pc = PromptController(prompt)
    isOI = pc.isOI()

    if isOI:
        oip = OIProcessor()
        oip.performWorkFlow(prompt)


def main():
    print(Msg.READY.value, flush=True)
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line == Msg.STOP:
                break
            if line.startswith(Msg.PROMPT):
                prompt = line[len(Msg.PROMPT) :].strip()
                prompt_pipeline(prompt)

    except (KeyboardInterrupt, EOFError):
        print(Msg.STOP.value, flush=True)


if __name__ == "__main__":
    main()
