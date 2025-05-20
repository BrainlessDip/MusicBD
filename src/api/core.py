from src.utils.logger import setup_logger
from quart import jsonify, request
from . import api_bp
logger = setup_logger("scrapers")

@api_bp.route('/', methods=['GET'])
async def main():
   return jsonify({"msg": "Backend of music bd"}), 200