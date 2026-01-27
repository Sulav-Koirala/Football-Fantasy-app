from fastapi import FastAPI
from app.routers import authentification,user,team,player,team_player
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(authentification.router)
app.include_router(user.router)
app.include_router(team.router)
app.include_router(player.router)
app.include_router(team_player.router)

@app.get("/")
def message():
    return {"Details": "Welcome, this is the laliga fantasy football app"}