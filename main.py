from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def cerca_su_vinted(query):
    url = f"https://www.vinted.it/catalog?search_text={query.replace(' ', '+')}"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9",
}

    response = requests.get(url, headers=headers)

# Stampa il codice HTML della pagina di Vinted nei log di Render
print("STATUS CODE:", response.status_code)
print("HTML RESPONSE:", response.text[:500])  # Stampiamo solo i primi 500 caratteri per non sovraccaricare i log



    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    risultati = soup.find_all("div", class_="feed-grid__item")[:5]

    annunci = []
    for risultato in risultati:
        titolo = risultato.find("span", class_="web_ui__Text__text")
        prezzo = risultato.find("span", class_="web_ui__Text__price")
        link = risultato.find("a", href=True)

        if titolo and prezzo and link:
            annunci.append({
                "titolo": titolo.text.strip(),
                "prezzo": prezzo.text.strip(),
                "link": "https://www.vinted.it" + link["href"]
            })

    return annunci

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Devi fornire un termine di ricerca."}), 400

    risultati = cerca_su_vinted(query)
    return jsonify(risultati)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
