from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .timing_middleware import TimingMiddleware

def setup_middlewares(app: FastAPI):
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Custom middleware
    app.add_middleware(TimingMiddleware)