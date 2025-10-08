from fastapi import FastAPI
from . import models
from .database import engine
from .routers import transactions # Import the transactions router

# This line tells SQLAlchemy to create all the tables defined in models.py
# that don't already exist in the database when the app starts.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transactions Microservice")

# Here we tell our main app to use all the endpoints from the transactions router.
app.include_router(
    transactions.router,
    prefix="/transactions", # All URLs in this router will start with /transactions
    tags=["Transactions"],  # This groups these endpoints in the API documentation
)

@app.get("/")
def read_root():
    """A simple endpoint to check if the service is running."""
    return {"message": "Transactions Microservice is running!"}

