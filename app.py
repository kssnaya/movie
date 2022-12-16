from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

client = MongoClient('mongodb+srv://admin:admin@cluster0.pjbjofm.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_recive = request.form['url_give']
    star_recive = request.form['star_give']
    comment_recive = request.form['comment_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_recive,headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')
    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    doc = {
        'image': image,
        'title': title,
        'description': description,
        'star': star_recive,
        'comment': comment_recive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
