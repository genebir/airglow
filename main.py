from fastapi import FastAPI
from uvicorn import run
import logging

log = logging.getLogger('airglow')

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    run('main:app', host='localhost', port=8000, reload=True)

