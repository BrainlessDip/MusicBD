from quart import Quart, jsonify, render_template
from src.api import api_bp

app = Quart(__name__)
app.register_blueprint(api_bp)

@app.route('/')
async def index():
    return await render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)