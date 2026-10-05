from fastapi import FastAPI

from routers import historia

app = FastAPI(title="Motor Narrativo - La Mina de Cristal Dormido")
app.include_router(historia.router)
