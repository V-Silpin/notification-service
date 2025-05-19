from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins if set to ["*"]
    allow_credentials=True,
    allow_methods=["POST"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the router with a prefix if needed
app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)