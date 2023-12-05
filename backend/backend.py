from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Update with your Svelte dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return ({"dara":"dinsid"})
@app.post('/login')
def login(data : dict):
    print("Data",data)
    return ({"dara":"dinsid"})