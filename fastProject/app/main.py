import time
from typing import Callable

from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, post, users, vote
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.middleware('http')
async def my_middleware(request: Request, call_next: Callable) -> Response:
    ip_address = request.client.host
    start = time.perf_counter()

    response = await call_next(request)

    end = time.perf_counter() - start
    print(f"Time execution: {end}")
    print(ip_address)
    return response


@app.get("/")
def root():
    time.sleep(2)
    return {"message": "Hello World my friend"}
