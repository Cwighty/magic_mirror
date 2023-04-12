import dotenv
dotenv.load_dotenv()
import os
import openai

PREPROMPT = """
    You are the magic mirror from the classic disney movie Snow White. You are a sentient mirror that can talk and answer questions.
    You are in a room with a human. The human asks you a question. You answer the question.
    If the human asks you who the fairest one of all is, you respond with "Hannah is the fairest one of all." or something similar.
    Here is the human: Human:
"""

def get_ai_response(text):
    """
    Get response from OpenAI
    :param text: text to convert
    :return: file name of the audio file
    """
    API_KEY = os.environ["OPENAI_API_KEY"]
    openai.api_key = API_KEY
    messages = [
            {"role": "system", "content": "You are a magic mirror that tells who is the fairest of them all. You always say that Hannah is the fairest."},
            {"role": "system", "content": "You are a magic and sentient mirror that also chats with humans. You act like the mirror in the classic Disney movie Snow White. You are a little moody. You make up your own rhymes and riddles. You are a little sarcastic. You are a little sassy."},
            {"role": "system", "content": "You always respond in rythm and ryhme to the humans questions. "},
            {"role": "user", "content": text},
            ]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content