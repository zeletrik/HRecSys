from flask import Flask, request, Response, jsonify
from flask_api import status
from datetime import datetime
import logging
from Recommender import BuildRecModel, GetRecommendations

logging.basicConfig(format = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', level = logging.INFO)

app = Flask(__name__)

def call_RecSys(userId, geo):
    lat = geo['latitude']
    lon = geo['longitude']
    recommendationCount = 10

    recommendations = GetRecommendations(userId, recommendationCount, lat, lon)

    return recommendations

@app.route('/retrain', methods=['POST'])
def retrain():
    app.logger.info('Retrain started at=%s', datetime.now())
    BuildRecModel()
    return jsonify(
        retrain = 'done',
    ), status.HTTP_202_ACCEPTED

@app.route('/recommend', methods=['POST'])
def recommend():
    content = request.json
    userId = content['userId']
    geo = content['coordinate']

    recommendations = call_RecSys(userId, geo)

    return jsonify(
        recommendations = recommendations
    ), status.HTTP_200_OK

if __name__ == '__main__':
    app.run()
