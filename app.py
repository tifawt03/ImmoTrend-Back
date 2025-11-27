from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from agent import ImmoTrendAgent

load_dotenv()

app = FastAPI(
    title="ImmoTrend API",
    description="API de prédiction immobilière avec IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
agent = ImmoTrendAgent(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "immotrend"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "port": os.getenv("DB_PORT", "5432")
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return None


class PredictionRequest(BaseModel):
    city: str
    neighborhood: Optional[str] = None
    include_projects: Optional[bool] = True

class ExternalFactors(BaseModel):
    projets_infrastructure: Optional[list] = []
    nouveaux_transports: Optional[list] = []
    zones_activite: Optional[list] = []
    evolution_population: Optional[float] = None


@app.get("/")
def root():
    return {"message": "ImmoTrend API v1.0", "status": "running"}


@app.get("/health")
def health_check():
    db_status = "connected" if get_db_connection() else "disconnected"
    return {
        "api": "healthy",
        "database": db_status,
        "groq_configured": bool(GROQ_API_KEY)
    }


@app.post("/predict")
def predict_price(request: PredictionRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY non configurée")
    
    conn = get_db_connection()
    historical_data = []
    external_factors = {}
    
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT date, prix_m2 
                    FROM prix_historique 
                    WHERE ville = %s 
                    ORDER BY date DESC 
                    LIMIT 24
                """, (request.city,))
                rows = cur.fetchall()
                # Convertir les dates en string !
                historical_data = [{"date": str(row["date"]), "prix_m2": float(row["prix_m2"])} for row in rows]
                
                if request.include_projects:
                    cur.execute("""
                        SELECT nom, type, date_prevue, impact_estime
                        FROM projets_urbains
                        WHERE ville = %s AND date_prevue > NOW()
                    """, (request.city,))
                    projects = cur.fetchall()
                    # Convertir les dates en string !
                    external_factors["projets"] = [
                        {
                            "nom": p["nom"],
                            "type": p["type"],
                            "date_prevue": str(p["date_prevue"]) if p["date_prevue"] else None,
                            "impact_estime": p["impact_estime"]
                        }
                        for p in projects
                    ]
                    
        except Exception as e:
            print(f"Erreur DB: {e}")
        finally:
            conn.close()
    
    if not historical_data:
        historical_data = get_demo_data(request.city)
    
    prediction = agent.predict(
        city=request.city,
        historical_data=historical_data,
        external_factors=external_factors if external_factors else None
    )
    
    return {
        "city": request.city,
        "prediction": prediction,
        "data_source": "database" if conn else "demo"
    }


@app.post("/analyze")
def analyze_market(city: str, factors: ExternalFactors):
    if not agent:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY non configurée")
    
    external = {
        "projets_infrastructure": factors.projets_infrastructure,
        "nouveaux_transports": factors.nouveaux_transports,
        "zones_activite": factors.zones_activite,
        "evolution_population": factors.evolution_population
    }
    
    historical_data = get_demo_data(city)
    
    prediction = agent.predict(
        city=city,
        historical_data=historical_data,
        external_factors=external
    )
    
    return {"city": city, "analysis": prediction}


@app.get("/cities")
def get_cities():
    conn = get_db_connection()
    
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT ville FROM prix_historique")
                cities = [row["ville"] for row in cur.fetchall()]
                return {"cities": cities}
        finally:
            conn.close()
    
    return {
        "cities": ["Montpellier", "Toulouse", "Carcassonne", "Perpignan"]
    }


@app.get("/history/{city}")
def get_price_history(city: str):
    conn = get_db_connection()
    
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT date, prix_m2 
                    FROM prix_historique 
                    WHERE ville = %s 
                    ORDER BY date
                """, (city,))
                rows = cur.fetchall()
                return {"city": city, "history": [{"date": str(r["date"]), "prix_m2": float(r["prix_m2"])} for r in rows]}
        finally:
            conn.close()
    
    return {"city": city, "history": get_demo_data(city)}


def get_demo_data(city: str) -> list:
    demo_prices = {
        "Montpellier": [
            {"date": "2023-04", "prix_m2": 3100},
            {"date": "2023-07", "prix_m2": 3150},
            {"date": "2023-10", "prix_m2": 3200},
            {"date": "2024-01", "prix_m2": 3250},
            {"date": "2024-04", "prix_m2": 3300},
        ],
        "Toulouse": [
            {"date": "2023-04", "prix_m2": 3200},
            {"date": "2023-07", "prix_m2": 3280},
            {"date": "2023-10", "prix_m2": 3350},
            {"date": "2024-01", "prix_m2": 3400},
            {"date": "2024-04", "prix_m2": 3424},
        ],
        "Carcassonne": [
            {"date": "2023-04", "prix_m2": 1350},
            {"date": "2023-07", "prix_m2": 1380},
            {"date": "2023-10", "prix_m2": 1410},
            {"date": "2024-01", "prix_m2": 1440},
            {"date": "2024-04", "prix_m2": 1461},
        ],
        "Perpignan": [
            {"date": "2023-04", "prix_m2": 1580},
            {"date": "2023-07", "prix_m2": 1610},
            {"date": "2023-10", "prix_m2": 1640},
            {"date": "2024-01", "prix_m2": 1660},
            {"date": "2024-04", "prix_m2": 1675},
        ],
    }
    return demo_prices.get(city, demo_prices["Montpellier"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)