import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Database connection
def get_db_connection():
	conn = sqlite3.connect('blog.db')
	conn.row_factory = sqlite3.Row
	return conn


# Initialize database
def init_db():
	with get_db_connection() as conn:
		conn.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )''')


init_db()


# CRUD operations
def read_blog_data():
	with get_db_connection() as conn:
		return conn.execute('SELECT * FROM posts').fetchall()


def write_blog_data(title, content):
	with get_db_connection() as conn:
		conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
		conn.commit()


def update_blog_data(post_id, title, content):
	with get_db_connection() as conn:
		conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
		conn.commit()


def delete_post(post_id):
	with get_db_connection() as conn:
		conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
		conn.commit()


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	blogs = read_blog_data()
	return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: int):
	blogs = read_blog_data()
	post = blogs[post_id] if 0 <= post_id < len(blogs) else None
	return templates.TemplateResponse("post.html", {"request": request, "post": post})


@app.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
	return templates.TemplateResponse("create_post.html", {"request": request})


@app.post("/create_post")
async def create_post(title: str = Form(...), content: str = Form(...)):
	write_blog_data(title, content)
	return RedirectResponse("/", status_code=303)


@app.get("/edit_post/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
	blogs = read_blog_data()
	post = blogs[post_id] if 0 <= post_id < len(blogs) else None
	return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})


@app.post("/edit_post/{post_id}")
async def edit_post(post_id: int, title: str = Form(...), content: str = Form(...)):
	update_blog_data(post_id, title, content)
	return RedirectResponse("/", status_code=303)


@app.post("/delete_post/{post_id}")
async def delete_post_confirmation(post_id: int):
	delete_post(post_id)
	return RedirectResponse("/", status_code=303)


init_db()
