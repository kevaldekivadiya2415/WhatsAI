from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import chatbot
import uvicorn

# Initialize the FastAPI application
app = FastAPI()

# Include CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatbot.router, prefix="")

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
