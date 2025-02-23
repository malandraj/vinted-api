import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# Funzione per cercare inserzioni su Vinted e analizzare l'HTML
def search_vinted(query):
    url = f"https://www.vinted.it/catalog?search={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.vinted.it/",
        "DNT": "1",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Trova tutte le inserzioni nella pagina
            items = []
            for item in soup.find_all("div", class_="web_ui__Cell__cell web_ui__Cell__narrow"):
  # Questo seleziona le inserzioni
                title_tag = item.find("h2")  # Trova il titolo
                price_tag = item.find("p", class_="price")  # Trova il prezzo
                link_tag = item.find("a", href=True)  # Trova il link

                if title_tag and price_tag and link_tag:
                    items.append({
                        "title": title_tag.text.strip(),
                        "price": price_tag.text.strip(),
                        "url": f"https://www.vinted.it{link_tag['href']}"
                    })

            return {"results": items}

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

# Route per testare se il server è attivo
@app.route('/')
def home():
    return jsonify({"message": "API Vinted attiva"}), 200
