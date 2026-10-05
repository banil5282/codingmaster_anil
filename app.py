from fastapi import FastAPI

# Create FastAPI instance
app = FastAPI()

# Define a GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}
