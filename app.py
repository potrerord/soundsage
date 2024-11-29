# import main Flask class and request object
from flask import Flask, request, jsonify
from requests import get_recommendations

# create the Flask app
app = Flask(__name__)

@app.route('/recommendations')
def get_recommendation():
    data = get_recommendations()
    return jsonify(data)

# Add query string for getting feedback
@app.route('/soundsage/feedback')
def get_feedback():
    return 'Form Data Example'

if __name__ == '__main__':
    # run app in debug mode on port 8080
    app.run(debug=True, port=8080)
