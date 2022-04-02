from typing import Optional

from fastapi import FastAPI

app = FastAPI(title='Eco-system for call-center')


@app.get("/")
def read_root():
    return {"index": "page"}

