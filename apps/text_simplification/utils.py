import json

import requests
import openai

# url = input("Please enter text simplification server link: ")
# openai.api_key = ""
url = ""


def openai_chatgpt_simplifier(text):
    simplification_prompt = """
You are a Text simplifier.
I want you to act as an English translator, spelling corrector, and simplifier. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and simplified version of my text, in English. I want you to replace my words and sentences with very easy, simple, and straightforward English words and sentences only. but keep the meaning stays the same. I want you to only reply to the correction, the simplification, and nothing else, do not write explanations.
Answer as concisely as possible.
    """.strip()
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": simplification_prompt},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content


def openai_gpt3_simplifier(text):
    simplification_prompt = "simplify this for a first-grade student in simple english"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{simplification_prompt}:\n\n {text}",
        temperature=0.7,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]["text"]


def our_simplifier(text):
    data = {"text": text}
    response = requests.post(url, json=data)
    try:
        output = json.loads(response.content.decode('utf-8'))['output']
    except Exception as error:
        raise Exception("Text Simplification Server Error, Check the Server Link")
    return output


def simplify_text(text, model="chatgpt"):
    result = ""
    model = model.lower()
    if not text.endswith("."):
        text += "."
    if model == "chatgpt":
        result = openai_chatgpt_simplifier(text)
    elif model == "gpt3":
        result = openai_gpt3_simplifier(text)
    elif model == "ours":
        result = our_simplifier(text)
    else:
        result = "Error!"
    return result.strip()
