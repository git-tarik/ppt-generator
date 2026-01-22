from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import generate

app = FastAPI(title="PPT Generator API - Phase 1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router)

@app.get("/")
def read_root():
    return {"message": "PPT Generator Backend is running. Phase 1 Dummy Mode."}
