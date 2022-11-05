from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()
@app.get('/')
def index():
    return RedirectResponse(url='/webapp-backend/static/index.html')

app.mount("/", StaticFiles(directory="../"), name="repo")
