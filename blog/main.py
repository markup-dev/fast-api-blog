from fastapi import FastAPI
from routers import router
from db import Base, engine

app = FastAPI()

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

# Подключение маршрутизатора к приложению
app.include_router(router)
