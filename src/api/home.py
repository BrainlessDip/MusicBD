from src.api import api_bp
from quart import jsonify, request
from src.utils.handle_requests import fetch_content
from urllib.parse import urlparse, unquote

@api_bp.route('/home', methods=['GET'])
async def home_page():
   soup = await fetch_content('https://music.com.bd/')
   data = {a.text.strip().split('\n')[0]: unquote(urlparse(a["href"]).path.rstrip('/')) for a in soup.find_all("a", class_="list-group-item")}
   return jsonify({"data": data}), 200