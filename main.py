import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Funzione per cercare inserzioni su Vinted
def search_vinted(query):
    url = f"https://www.vinted.it/vinted/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.vinted.it/",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()  # Assumendo che Vinted restituisca un JSON
        else:
            return {"error": "Request failed", "status_code": response.status_code}
    
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}

# Endpoint API
@app.route('/vinted/search', methods=['GET'])
def api_search():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400

    result = search_vinted(query)
    return jsonify(result)


