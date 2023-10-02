from fastapi import FastAPI

app = FastAPI(title="Fake Backend")


@app.get("/")
def hello_world():
    return {"data": "hello world!"}
