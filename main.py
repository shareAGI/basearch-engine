from fastapi import FastAPI
from app.api.v1 import emb
from app.core.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(emb.router, prefix="/v1/emb", tags=["emb"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
