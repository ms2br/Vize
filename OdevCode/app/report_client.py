import requests
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

API_URL = "http://127.0.0.1:5001/report/top_recommended_movies"

app = FastAPI()
app.mount("/static", StaticFiles(directory="Style"), name="static")
templates = Jinja2Templates(directory="Templates")


def fetch_movies(limit=3):
    r = requests.get(API_URL, params={"limit": limit}, timeout=5)
    r.raise_for_status()
    return r.json()


@app.get("/admin", response_class=HTMLResponse)
@app.get("/admin/", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    movies = fetch_movies(limit=3)

    total_recommendations = sum(m["count"] for m in movies)
    avg_imdb = round(
        sum(m["imdb"] for m in movies) / len(movies),
        1
    )

    top_movie = movies[0]["title"]

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "movies": movies,
            "total": total_recommendations,
            "avg_imdb": avg_imdb,
            "top_movie": top_movie
        }
    )