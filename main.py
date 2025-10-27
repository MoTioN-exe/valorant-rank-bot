from flask import Flask, Response
import requests
import os
import sys

app = Flask(__name__)

# Configuration depuis les variables d'environnement
VALORANT_API_KEY = os.getenv("VALORANT_API_KEY")
VALORANT_API_URL = os.getenv("VALORANT_API_URL", "https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{name}/{tag}")
VALORANT_REGION = os.getenv("VALORANT_REGION", "eu")
DEFAULT_PLAYER_NAME = os.getenv("DEFAULT_PLAYER_NAME", "MoTioN")
DEFAULT_PLAYER_TAG = os.getenv("DEFAULT_PLAYER_TAG", "0807")

if not VALORANT_API_KEY:
    print("ERREUR: La variable d'environnement VALORANT_API_KEY n'est pas définie.", file=sys.stderr)
    sys.exit(1)

@app.route('/')
def get_valorant_rank():
    """
    Endpoint principal qui récupère le rang Valorant et le retourne au format texte simple.
    Format: MoTioN#0807 – Immortal I – 75 RR
    """
    player_name = DEFAULT_PLAYER_NAME
    player_tag = DEFAULT_PLAYER_TAG
    
    try:
        url = VALORANT_API_URL.format(region=VALORANT_REGION, name=player_name, tag=player_tag)
        headers = {
            "Authorization": VALORANT_API_KEY
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        # Vérification de la réponse
        if response.status_code == 200:
            data = response.json()
            
            # Extraction des données
            if data.get("status") == 200 and "data" in data:
                player_data = data["data"]
                
                # Récupération du rang actuel
                current_data = player_data.get("current_data", {})
                rank_name = current_data.get("currenttierpatched", "Unknown")
                rr = current_data.get("ranking_in_tier", 0)
                
                # Formatage du texte (sans le pseudo)
                formatted_text = f"{rank_name} – {rr} RR"
                
                return Response(formatted_text, mimetype='text/plain')
            else:
                error_msg = f"Erreur: Joueur non trouvé ou données invalides"
                return Response(error_msg, mimetype='text/plain', status=404)
        
        elif response.status_code == 404:
            error_msg = f"{player_name}#{player_tag} – Joueur non trouvé"
            return Response(error_msg, mimetype='text/plain', status=404)
        
        else:
            error_msg = f"Erreur API: {response.status_code}"
            return Response(error_msg, mimetype='text/plain', status=response.status_code)
            
    except requests.exceptions.Timeout:
        error_msg = "Erreur: Timeout de l'API Valorant"
        return Response(error_msg, mimetype='text/plain', status=504)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erreur de connexion: {str(e)}"
        return Response(error_msg, mimetype='text/plain', status=503)
    
    except Exception as e:
        error_msg = f"Erreur interne: {str(e)}"
        return Response(error_msg, mimetype='text/plain', status=500)

@app.route('/rank/<name>/<tag>')
def get_custom_rank(name, tag):
    """
    Endpoint optionnel pour récupérer le rang d'un joueur spécifique.
    Usage: /rank/MoTioN/0807
    """
    try:
        url = VALORANT_API_URL.format(region=VALORANT_REGION, name=name, tag=tag)
        headers = {
            "Authorization": VALORANT_API_KEY
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == 200 and "data" in data:
                player_data = data["data"]
                current_data = player_data.get("current_data", {})
                rank_name = current_data.get("currenttierpatched", "Unknown")
                rr = current_data.get("ranking_in_tier", 0)
                
                formatted_text = f"{rank_name} – {rr} RR"
                return Response(formatted_text, mimetype='text/plain')
            else:
                error_msg = f"{name}#{tag} – Données invalides"
                return Response(error_msg, mimetype='text/plain', status=404)
        
        elif response.status_code == 404:
            error_msg = f"{name}#{tag} – Joueur non trouvé"
            return Response(error_msg, mimetype='text/plain', status=404)
        
        else:
            error_msg = f"Erreur API: {response.status_code}"
            return Response(error_msg, mimetype='text/plain', status=response.status_code)
            
    except requests.exceptions.Timeout:
        error_msg = "Erreur: Timeout de l'API Valorant"
        return Response(error_msg, mimetype='text/plain', status=504)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erreur de connexion"
        return Response(error_msg, mimetype='text/plain', status=503)
    
    except Exception as e:
        error_msg = f"Erreur interne"
        return Response(error_msg, mimetype='text/plain', status=500)

if __name__ == '__main__':
    # Bind à 0.0.0.0:5000 pour être accessible depuis l'extérieur
    app.run(host='0.0.0.0', port=5000, debug=False)
