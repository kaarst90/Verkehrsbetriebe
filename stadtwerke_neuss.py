import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_stadtwerke_neuss():
    url = "https://www.stadtwerke-neuss.de/nahverkehr/fahrplan"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    lines = []
    for line in soup.find_all('div', class_='line'):
        line_name = line.find('h3').text
        stops = [stop.text for stop in line.find_all('li')]
        lines.append({'line': line_name, 'stops': stops})
    return lines

def save_to_db(data):
    conn = sqlite3.connect('transportation_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stadtwerke_neuss
                      (line TEXT, stops TEXT)''')
    for entry in data:
        cursor.execute("INSERT INTO stadtwerke_neuss (line, stops) VALUES (?, ?)",
                       (entry['line'], ', '.join(entry['stops'])))
    conn.commit()
    conn.close()

data = scrape_stadtwerke_neuss()
save_to_db(data)
