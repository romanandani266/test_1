from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="[Insert Project Name Here]", description="Backend API for [Insert Project Name Here]")

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class Feature1Request(BaseModel):
    param1: str
    param2: int

class Feature1Response(BaseModel):
    result: str

class Feature2Request(BaseModel):
    param1: str
    param2: Optional[bool] = False

class Feature2Response(BaseModel):
    status: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the [Insert Project Name Here] API!"}

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/feature1", response_model=Feature1Response)
async def feature1_endpoint(request: Feature1Request):
    if not request.param1 or request.param2 < 0:
        raise HTTPException(status_code=400, detail="Invalid input parameters")
    return Feature1Response(result=f"Processed {request.param1} with value {request.param2}")

@app.post("/feature2", response_model=Feature2Response)
async def feature2_endpoint(request: Feature2Request):
    if not request.param1:
        raise HTTPException(status_code=400, detail="param1 is required")
    return Feature2Response(status="success", data={"param1": request.param1, "param2": request.param2})

@app.get("/feature3")
async def feature3_endpoint():
    return {"message": "Feature 3 is under development"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/docs")
async def get_documentation():
    return {"message": "Visit /docs or /redoc for API documentation"}