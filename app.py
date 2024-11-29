# import main Flask class and request object
from flask import Flask, request, jsonify
from requests import get_recommendations, feedback_system

# create the Flask app
app = Flask(__name__)

@app.route('/recommendations')
def get_recommendation():
    data = get_recommendations('1')
    return jsonify(data)

# Add query string for getting feedback
@app.route('/feedback', methods=["POST"], strict_slashes=False)
def get_feedback():
    song_info = request.json['song']
    feedback = request.json['rating']
    user_id = request.json['user_id']
    feedback_system(song_info, feedback, user_id)
    return 'Done', 201

if __name__ == '__main__':
    # run app in debug mode on port 8080
    app.run(debug=True, port=8080)
