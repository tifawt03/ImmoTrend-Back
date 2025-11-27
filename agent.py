from groq import Groq
import json

class ImmoTrendAgent:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        
        self.system_prompt = """Tu es un expert en analyse immobilière française. 
Tu analyses les données du marché pour prédire les prix au m².

CONTEXTE DE TON EXPERTISE :
- Tu connais parfaitement le marché immobilier du sud de la France
- Tu analyses les tendances historiques des prix
- Tu prends en compte les facteurs économiques locaux
- Tu considères les projets d'urbanisme et d'infrastructure

QUAND ON TE DONNE DES DONNÉES, TU DOIS :
1. Analyser l'évolution historique des prix
2. Identifier la tendance (hausse, baisse, stable)
3. Considérer les facteurs externes (projets, transports, etc.)
4. Donner une estimation du prix futur avec un intervalle de confiance

FORMAT DE RÉPONSE (JSON obligatoire) :
{
    "prix_estime": <nombre en €/m²>,
    "intervalle_bas": <nombre>,
    "intervalle_haut": <nombre>,
    "tendance": "hausse" | "baisse" | "stable",
    "confiance": <pourcentage 0-100>,
    "facteurs_positifs": ["facteur1", "facteur2"],
    "facteurs_negatifs": ["facteur1", "facteur2"],
    "analyse": "<explication courte de ton raisonnement>"
}

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""

    def predict(self, city: str, historical_data: list, external_factors: dict = None) -> dict:
        """
        Fait une prédiction de prix pour une ville donnée.
        """
        user_prompt = f"""Analyse le marché immobilier de {city}.

DONNÉES HISTORIQUES DES PRIX AU M² :
{json.dumps(historical_data, indent=2, ensure_ascii=False)}

"""
        if external_factors:
            user_prompt += f"""FACTEURS EXTERNES À CONSIDÉRER :
{json.dumps(external_factors, indent=2, ensure_ascii=False)}

"""
        user_prompt += "Donne-moi ta prédiction pour les 6 prochains mois."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return json.loads(result)
            
        except json.JSONDecodeError:
            return {
                "error": "Réponse mal formatée",
                "raw_response": response.choices[0].message.content
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze_zone(self, city: str, neighborhood: str, data: dict) -> dict:
        """
        Analyse approfondie d'une zone spécifique.
        """
        user_prompt = f"""Fais une analyse approfondie du quartier {neighborhood} à {city}.

DONNÉES DU MARCHÉ :
- Prix moyen actuel : {data.get('prix_moyen', 'N/A')} €/m²
- Évolution sur 1 an : {data.get('evolution_1an', 'N/A')}%
- Nombre de transactions : {data.get('transactions', 'N/A')}
- Type de biens majoritaire : {data.get('type_biens', 'N/A')}

PROJETS DANS LA ZONE :
{json.dumps(data.get('projets', []), indent=2, ensure_ascii=False)}

Donne ta prédiction et tes recommandations."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": str(e)}
