from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_download_link(url):
    """Scrape the MediaFire page to find the direct download link."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    download_link_element = soup.find('a', {'id': 'downloadButton'})
    if download_link_element:
        return download_link_element['href']
    return None

def extract_id_and_filename(mediafire_url):
    """Extract the file ID and filename from a MediaFire URL."""
    pattern = r"https://www\.mediafire\.com/file/([a-zA-Z0-9]+)/(.+?)/file"
    match = re.match(pattern, mediafire_url)
    if match:
        file_id, filename = match.groups()
        return file_id, filename
    return None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    mediafire_url = request.form['mediafire_url']
    file_id, filename = extract_id_and_filename(mediafire_url)
    
    if file_id and filename:
        download_url = url_for('download', id=file_id, filename=filename, _external=True)
        return f'Direct Download Link: <a href="{download_url}">{download_url}</a>'
    else:
        return "Invalid MediaFire URL. Please try again."

@app.route('/download')
def download():
    file_id = request.args.get('id')
    filename = request.args.get('filename')
    
    if not file_id or not filename:
        return "Missing parameters."
    
    mediafire_url = f"https://www.mediafire.com/file/{file_id}/{filename}/file"
    direct_download_link = get_download_link(mediafire_url)
    
    if direct_download_link:
        return redirect(direct_download_link, code=302)
    else:
        return "Failed to retrieve the direct download link."

if __name__ == '__main__':
    app.run(debug=True)
