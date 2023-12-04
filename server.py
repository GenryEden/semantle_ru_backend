from model import model
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from cryptography.fernet import Fernet
import random

file = open('dataset.txt', 'r')
words = [word[:-1] for word in file]

fernetKey = Fernet.generate_key()
fernet = Fernet(fernetKey)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/random_word")
def random_word() -> bytes:
    while True:
        word = random.choice(words)
        if not word + "_NOUN" in model:
            continue
        mostSimilar = model.most_similar(word + "_NOUN", topn=1)[0]
        if mostSimilar[1] < 0.7 or not mostSimilar[0].endswith("_NOUN"):
            continue
        return fernet.encrypt(random.choice(words).encode())

@app.get("/similarity")
def similarity(encWord: bytes, word: str) -> float:
    return float(model.similarity(
        fernet.decrypt(encWord).decode('utf-8') + "_NOUN",
        word.lower() + "_NOUN"
    ))

@app.get("/check")
def check(encWord: bytes, word: str) -> bool:
    return fernet.decrypt(encWord).decode('utf-8') == word.lower()

@app.get("/hint")
def hint(encWord: bytes, bestGuess: float):
    try:
        hints = [
            entry for entry in model.most_similar(
                fernet.decrypt(encWord).decode('utf-8') + "_NOUN",
                topn=100
            ) if entry[1] > bestGuess
        ]
        hint = random.choice(hints)
        return (hint[0].split('_')[0], hint[1])
    except IndexError:
        return None
