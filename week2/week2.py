from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

posts = []

@app.route('/')
def home():
    return render_template('week2.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    post = {
        'title': data['title'],
        'content': data['content'],
        'date': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }
    posts.insert(0, post)
    return jsonify(post)

if __name__ == '__main__':
    app.run(debug=True)