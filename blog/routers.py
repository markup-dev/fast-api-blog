from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from db import get_db
from models import Post

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Маршруты
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
	"""
	Отображает главную страницу со списком постов блога.

	Args:
			request (Request): Объект запроса.
			db (Session): Сессия базы данных.

	Returns:
			HTMLResponse: Ответ с отрисованным шаблоном.
	"""
	blogs = db.query(Post).all()
	return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})


@router.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int, db: Session = Depends(get_db)):
	"""
	Отображает полный пост по его идентификатору.

	Args:
			request (Request): Объект запроса.
			post_id (int): Идентификатор поста.
			db (Session): Сессия базы данных.

	Returns:
			HTMLResponse: Ответ с отрисованным шаблоном поста.

	Raises:
			HTTPException: Если пост не найден.
	"""
	post = db.query(Post).filter(Post.id == post_id).first()
	if post is None:
		raise HTTPException(status_code=404, detail="Post not found")
	return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
	"""
	Отображает форму для создания нового поста.

	Args:
			request (Request): Объект запроса.

	Returns:
			HTMLResponse: Ответ с отрисованным шаблоном формы создания поста.
	"""
	return templates.TemplateResponse("create_post.html", {"request": request})


@router.post("/create_post")
async def create_post(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
	"""
	Создаёт новый пост в базе данных.

	Args:
			title (str): Заголовок поста.
			content (str): Содержимое поста.
			db (Session): Сессия базы данных.

	Returns:
			RedirectResponse: Перенаправление на главную страницу после создания поста.
	"""
	new_post = Post(title=title, content=content)
	db.add(new_post)
	db.commit()
	return RedirectResponse("/", status_code=303)


@router.get("/edit_post/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
	"""
	Отображает форму для редактирования существующего поста.

	Args:
			request (Request): Объект запроса.
			post_id (int): Идентификатор поста.
			db (Session): Сессия базы данных.

	Returns:
			HTMLResponse: Ответ с отрисованным шаблоном формы редактирования поста.

	Raises:
			HTTPException: Если пост не найден.
	"""
	post = db.query(Post).filter(Post.id == post_id).first()
	if post is None:
		raise HTTPException(status_code=404, detail="Post not found")
	return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})


@router.post("/edit_post/{post_id}")
async def edit_post(post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
	"""
	Обновляет существующий пост в базе данных.

	Args:
			post_id (int): Идентификатор поста.
			title (str): Новый заголовок поста.
			content (str): Новое содержимое поста.
			db (Session): Сессия базы данных.

	Returns:
			RedirectResponse: Перенаправление на главную страницу после обновления поста.

	Raises:
			HTTPException: Если пост не найден.
	"""
	post = db.query(Post).filter(Post.id == post_id).first()
	if post is None:
		raise HTTPException(status_code=404, detail="Post not found")

	post.title = title
	post.content = content
	db.commit()

	return RedirectResponse("/", status_code=303)


@router.get("/delete_post/{post_id}", response_class=HTMLResponse)
async def delete_post_confirmation(request: Request, post_id: int, db: Session = Depends(get_db)):
	"""
	Отображает страницу подтверждения удаления поста.

	Args:
			request (Request): Объект запроса.
			post_id (int): Идентификатор поста.
			db (Session): Сессия базы данных.

	Returns:
			HTMLResponse: Ответ с отрисованным шаблоном подтверждения удаления.

	Raises:
			HTTPException: Если пост не найден.
	"""
	post = db.query(Post).filter(Post.id == post_id).first()
	if post is None:
		raise HTTPException(status_code=404, detail="Post not found")

	return templates.TemplateResponse("confirm_delete.html", {"request": request, "post": post})


@router.post("/delete_post/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db)):
	"""
	Удаляет существующий пост из базы данных.

	Args:
			post_id (int): Идентификатор поста.
			db (Session): Сессия базы данных.

	Returns:
			RedirectResponse: Перенаправление на главную страницу после удаления поста.

	Raises:
			HTTPException: Если пост не найден.
	"""
	post = db.query(Post).filter(Post.id == post_id).first()

	if post is None:
		raise HTTPException(status_code=404, detail="Post not found")

	db.delete(post)
	db.commit()

	return RedirectResponse("/", status_code=303)
