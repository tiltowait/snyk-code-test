"""Some simple, insecure code."""

import db
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import BlogPost

app = FastAPI(title="Unsafe", description="Some slow pitches for SAST scanners", debug=True)
templates = Jinja2Templates(directory="templates")

db.create_table()


@app.post("/post/insert", tags=["XSS", "Unsafe"])
async def insert_post(post: BlogPost):
    """Insert a post into the database without any sanitization."""
    db.insert_post(post.title, post.content)
    return {"message": "Post created!"}


@app.get("/unsafe/post/{post_id}", response_class=HTMLResponse, tags=["XSS", "Unsafe"])
async def unsafe_display_post(request: Request, post_id: int):
    """Display a post without escaping the content."""
    post = db.get_post(post_id)
    return templates.TemplateResponse(
        request=request,
        name="post.html.jinja",
        context={"post": post, "escape": False},
    )


@app.get("/sql-injection", tags=["SQL Injection", "Unsafe"])
async def sql_injection(title: str):
    post = db.vulnerable_get_post_by_title(title)
    return post


@app.get("/path-traversal", tags=["Path Traversal", "Unsafe"], response_class=HTMLResponse)
async def path_traversal(request: Request, path="main.py"):
    """Read a file from the filesystem."""
    with open(path) as f:
        contents = f.read()
    return templates.TemplateResponse(
        request=request,
        name="path-traversal.html.jinja",
        context=dict(filename=path, contents=contents),
    )


@app.get("/add-two-numbers", tags=["Code Injection", "Unsafe"])
async def code_injection(first: str, second: str):
    """Execute some code using eval."""
    result = eval(f"{first} + {second}")
    return {"result": result}
