from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to get DB session
def get_db():
	"""
	Функция-генератор для получения сессии базы данных.

	Используется в маршрутах FastAPI как зависимость. Создаёт новую сессию
	и гарантирует её закрытие после завершения работы.

	Returns:
			Generator: Генератор, который выдаёт объект сессии базы данных.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
