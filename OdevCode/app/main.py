import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from api.recommend import router as recommend_router
from core.recommender import recommend_for_user, ratings, movies

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "Templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "Style")), name="static")
app.include_router(recommend_router)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    matched_user = ratings[
        (ratings['userName'] == username) &
        (ratings['password'] == password)
    ]
    if matched_user.empty:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Geçersiz kullanıcı adı veya şifre!"}
        )

    request.session["user_id"] = int(matched_user["userId"].iloc[0])
    return RedirectResponse("/dashboard", status_code=302)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse("/", status_code=302)

    recommendations = recommend_for_user(user_id)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "recommendations": recommendations,
            "user_id": user_id
        }
    )

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)



@app.get("/report/top_recommended_movies")
def report_top_movies(limit: int = 3):
    top_movies = (
        movies
        .sort_values(by="counter", ascending=False)
        .head(limit)
    )

    result = [
        {
            "title": row["title"],
            "count": int(row["counter"]),
            "imdb": float(row["imdb"])
        }
        for _, row in top_movies.iterrows()
    ]

    return JSONResponse(result)