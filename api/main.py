from typing import Union

from fastapi import FastAPI

app = FastAPI()


def run_api():
    @app.get("/")
    def read_root():
        return "Welcome to ACT API. For docs go to: ./docs"

    @app.get("/users/{id}")
    def read_item(id: int, q: Union[str, None] = None):
        return {"id": id}


if __name__ == "__main__":
    run_api()
