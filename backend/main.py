from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://yourfrontend.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginRequest(BaseModel):
    username: str
    password: str

class PricingRequest(BaseModel):
    product_id: str
    market_conditions: Dict[str, float]
    competitor_prices: Dict[str, float]

class PromotionRequest(BaseModel):
    promotion_id: str
    historical_data: List[Dict[str, float]]

class TradeSpendRequest(BaseModel):
    spend_id: str
    spend_details: Dict[str, float]

class CompetitorPriceRequest(BaseModel):
    competitor_id: str
    product_id: str

class RevenueForecastRequest(BaseModel):
    scenario_details: Dict[str, float]

mock_users = {
    "admin": "password123",
    "user1": "userpassword"
}

@app.get("/")
def read_root():
    return {"message": "Welcome to the PepsiCo NRM Optimization Platform API"}

@app.post("/login")
def login(request: LoginRequest):
    if request.username in mock_users and mock_users[request.username] == request.password:
        return {"message": "Login successful", "username": request.username}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/pricing/optimize")
def optimize_pricing(request: PricingRequest):
    optimized_price = sum(request.market_conditions.values()) / len(request.market_conditions) * 1.1
    return {
        "product_id": request.product_id,
        "optimized_price": round(optimized_price, 2),
        "competitor_prices": request.competitor_prices
    }

@app.post("/promotions/analyze")
def analyze_promotion(request: PromotionRequest):
    roi = sum(data["revenue"] for data in request.historical_data) / sum(data["spend"] for data in request.historical_data)
    return {
        "promotion_id": request.promotion_id,
        "roi": round(roi, 2),
        "recommendation": "Increase budget" if roi > 1.5 else "Reassess strategy"
    }

@app.post("/trade-spend/optimize")
def optimize_trade_spend(request: TradeSpendRequest):
    optimized_spend = {key: value * 0.9 for key, value in request.spend_details.items()}
    return {
        "spend_id": request.spend_id,
        "optimized_spend": optimized_spend
    }

@app.post("/competitor/track")
def track_competitor_price(request: CompetitorPriceRequest):
    competitor_price = 1.05 * 100
    return {
        "competitor_id": request.competitor_id,
        "product_id": request.product_id,
        "competitor_price": competitor_price
    }

@app.post("/revenue/forecast")
def forecast_revenue(request: RevenueForecastRequest):
    forecasted_revenue = sum(request.scenario_details.values()) * 1.2
    return {
        "forecasted_revenue": round(forecasted_revenue, 2),
        "scenario_details": request.scenario_details
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}