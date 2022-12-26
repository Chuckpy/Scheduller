from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from os import getenv
from core.apps.auth.app import router as auth_router
from core.apps.tasks.app import router as tasks_router
import uvicorn




def get_application() -> FastAPI:

    origins = [
        "http://localhost:3000",
        "localhost:3000",
    ]

    app = FastAPI()

    app.include_router(auth_router)
    app.include_router(tasks_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app


app = get_application()


@app.get("/")
async def read_root(request: Request):
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=int(getenv("PORT")),
        reload=getenv("DEBUG",False)
    )


