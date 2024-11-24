from sqlalchemy import Column, Integer, String
from db import Base


# Определение модели поста
class Post(Base):
	"""
	Модель Post представляет собой структуру данных для хранения информации о блоге.

	Атрибуты:
			id (int): Уникальный идентификатор поста. Является первичным ключом
			title (str): Заголовок поста. Не может быть пустым
			content (str): Содержимое поста. Не может быть пустым
	"""

	__tablename__ = 'posts'  # Имя таблицы в базе данных

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	content = Column(String, nullable=False)
