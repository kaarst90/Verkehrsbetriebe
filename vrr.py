import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_vrr():
    url = "https://www.vrr.de/de/fahrplan-mobilitaet/fahrplanauskunft/app/departureMonitor?formik=origin%3Dde%253A05162%253A20369&lng=de"
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS vrr
                      (line TEXT, stops TEXT)''')
    for entry in data:
        cursor.execute("INSERT INTO vrr (line, stops) VALUES (?, ?)",
                       (entry['line'], ', '.join(entry['stops'])))
    conn.commit()
    conn.close()

data = scrape_vrr()
save_to_db(data)
