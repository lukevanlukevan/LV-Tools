import hou
import openai
import os
from dotenv import load_dotenv, find_dotenv


def setKey():
    pbase = os.getcwd()
    pdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pdir)
    load_dotenv(find_dotenv())

    pbase = os.getcwd()
    pdir = os.path.dirname(os.path.abspath(__file__))
    key = os.getenv("OPENAI_KEY")
    # print(key)
    os.chdir(pbase)
    if key == "" or key == None:
        c, val = hou.ui.readInput("Please acquire OpenAI key and paste here", buttons=("Ok", "Cancel",), title="Open AI Key", close_choice=1)
        if c == 0:
            os.chdir(pdir)
            with open(".env", "w") as f:
                f.write("OPENAI_KEY=" + val)
            os.chdir(pbase)
            key = val


def call():
    setKey()
    key = os.getenv("OPENAI_KEY")
    if (key == ""):
        # print("OpenAI key is not set")
        pass
    else:
        openai.api_key = key
        node = hou.selectedNodes()[0]
        snippet = node.parm("snippet")

        print("GPT-3 is running...")

        initial = snippet.eval()

        snippet.set("// Running GPT-3...\n\n" + initial)

        response = openai.chat.completions.create(
            messages=[{"role": "system", "content": "you are are a code solving robot. I return only code blocks"},
                      {"role": "user", "content": "add comments to this houdini vex code: ```\n" + initial + "\n``` do not return anything other than code block. do not explain answer"}],
            model="gpt-3.5-turbo",

        )
        resp = response.choices[0].message.content.split("```")
        a = resp[1] if resp[0] == "" else resp[0]
        snippet.set(a.split("\n", 1)[1])
