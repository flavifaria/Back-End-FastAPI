#para istalar as bibliotecas para criação da API vamos usar
#pip install fastapi , uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensagem":"Merceária do Erinaldo"}