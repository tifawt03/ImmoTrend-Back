# ImmoTrend Backend - API de prédiction immobilière

Backend FastAPI avec agent IA Groq pour la prédiction des prix immobiliers.

## 🚀 Installation

### Prérequis
- Python 3.11+
- Docker (optionnel)
- Une clé API Groq

### 1. Obtenir une clé API Groq (gratuit)

1. Allez sur [console.groq.com](https://console.groq.com)
2. Créez un compte gratuit
3. Allez dans **API Keys** → **Create API Key**
4. Copiez la clé (commence par `gsk_...`)

### 2. Configuration

Créez un fichier `.env` à la racine du projet :
```env
GROQ_API_KEY=gsk_votre_cle_api_ici

DB_HOST=db
DB_NAME=immotrend
DB_USER=postgres
DB_PASSWORD=immotrend2024
DB_PORT=5432
```

### 3. Lancer avec Docker
```bash
docker-compose up --build
```

### 4. Lancer sans Docker
```bash
pip install -r requirements.txt
python app.py
```

## 📡 Endpoints API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Vérifier le status de l'API |
| GET | `/cities` | Liste des villes disponibles |
| GET | `/history/{city}` | Historique des prix d'une ville |
| POST | `/predict` | Prédiction IA pour une ville |

### Exemple de prédiction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"city": "Montpellier"}'
```

## 🤖 Agent IA

L'agent utilise **Groq** avec le modèle `llama-3.1-70b-versatile` pour analyser :
- L'historique des prix au m²
- Les projets urbains à venir
- Les facteurs économiques locaux

Et fournit :
- Une estimation de prix à 6 mois
- Un intervalle de confiance
- Une analyse détaillée des facteurs

## 📁 Structure
```
backend/
├── app.py              # API FastAPI
├── agent.py            # Agent IA Groq
├── requirements.txt    # Dépendances Python
├── Dockerfile          # Image Docker
└── .env                # Variables d'environnement (à créer)
```