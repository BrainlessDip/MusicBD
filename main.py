import os
from quart import Quart, jsonify, render_template,send_from_directory
from src.api import api_bp

app = Quart(__name__)
app.register_blueprint(api_bp)

@app.route('/')
async def index():
    return await render_template("index.html")

@app.route('/<folder>/<path:filename>')
async def serve_assets(folder, filename):
    path = os.path.join(f'templates/{folder}', filename)
    if not os.path.isfile(path):
        return {"error": "File not found"}, 404
    return await send_from_directory(f'templates/{folder}', filename)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)