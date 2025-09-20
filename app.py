from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_jkpsc_notifications():
    url = 'https://jkpsc.nic.in'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    notifications = []
    for a_tag in soup.find_all('a'):
        title = a_tag.text.strip()
        href = a_tag.get('href')
        if title and href:
            if href.startswith('/'):
                href = url + href
            if href.startswith('http'):
                notifications.append({'title': title, 'link': href})
    return notifications

@app.route('/')
def index():
    return "JKPSC Notifications API is running. Visit /api/notifications to see the data."

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    # Scrape fresh notifications on each request
    notifications = scrape_jkpsc_notifications()
    return jsonify(notifications)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
