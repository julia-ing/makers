from datetime import datetime

from bson import ObjectId
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

# test - 01

import re
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbmakers

my_date = datetime.now().strftime("%d")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/news')
def news():
    req = requests.get('https://www.boannews.com/media/list.asp')
    soup = BeautifulSoup(req.text, 'html.parser')
    myList = []
    items = soup.findAll("div", {"class": "news_list"})

    for item in items:
        title = item.select_one("span", {"class": "news_txt"}).text
        abbr = item.select_one("a.news_content").text
        title_url = item.find("a")["href"]
        sub_str = "https://www.boannews.com" + title_url
        sub_html = requests.get(url=sub_str)
        sub_obj = BeautifulSoup(sub_html.content, "html.parser")
        sub_news_text = str(sub_obj.select_one('#news_content > b'))
        sub_news_text = re.sub('<.+?>', ' / ', sub_news_text, 0).strip()
        news_date = sub_obj.select_one('#news_util01').text[24:27]
        item_info = {
            'title': title,
            'abbr': abbr,
            'sub_news_text': sub_news_text,
            'sub_str': sub_str,
        }
        if int(my_date) == int(news_date):
            myList.append(item_info)
    req2 = requests.get('https://www.boannews.com/media/o_list.asp')
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    week_list = []
    week_items = soup2.findAll("div", {"class": "news_list"})

    for item in week_items:
        title = item.select_one("span", {"class": "news_txt"}).text
        title_url = item.find("a")["href"]
        sub_str = "https://www.boannews.com" + title_url
        item_info = {
            'title': title,
            'sub_str': sub_str,
        }
        week_list.append(item_info)

    return render_template('news.html', list=myList, week_list=week_list)


@app.route('/contest')
def contest():
    req = requests.get('https://www.contestkorea.com/sub/list.php?displayrow=12&Txt_sGn=1&Txt_key=all&Txt_word=&Txt_bcode=030210001&Txt_code1=&Txt_aarea=&Txt_area=&Txt_sortkey=a.str_aedate&Txt_sortword=desc&Txt_chocode=&Txt_unicode')
    soup = BeautifulSoup(req.text, 'html.parser')
    myList = []
    items = soup.select('#frm > div > div.list_style_2 > ul > li')

    for item in items:
        category = item.select_one('div.title > a > span.category').text
        title = item.select_one('div.title > a > span.txt').text
        host = item.select_one('ul > li.icon_1').text
        date = item.select_one('div.date > div').text
        d_day = item.select_one('div.d-day.orange').text[:5]
        title_url = item.find("a")["href"]
        sub_str = "https://www.contestkorea.com/sub/" + title_url
        item_info = {
            'category': category,
            'title': title,
            'host': host,
            'date': date,
            'd_day': d_day,
            'sub_str': sub_str,
        }
        myList.append(item_info)

    return render_template('contest.html', list=myList)


@app.route('/job')
def job():
    return render_template('job.html')


@app.route('/job/memo', methods=['GET'])
def job_listing():
    jobs = list(db.jobs.find({}, {'_id': False}))
    return jsonify({'jobs': jobs})


@app.route('/job/memo', methods=['POST'])
def job_saving():
    url_receive = request.form['url_give']
    memo_receive = request.form['memo_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': title,
        'image': image,
        'url': url_receive,
        'memo': memo_receive
    }
    db.jobs.insert_one(doc)
    return jsonify({'msg': '저장이 완료되었습니다!'})


@app.route('/study', methods=['GET'])
def study():
    return render_template("study.html")


@app.route('/study/<category>/sub', methods=['GET'])
def study_sub(category):
    data = db.categories.find_one({"category": category})
    print(data)
    return render_template("study_sub.html", data=data)


@app.route('/study/add', methods=['GET'])
def study_listing():
    categories = list(db.categories.find({}, {'_id': False}))
    return jsonify({'categories': categories})


@app.route('/study/add', methods=['POST'])
def study_saving():
    category_receive = request.form['category_give']
    level_receive = request.form['level_give']
    doc = {
        'category': category_receive,
        'level': int(level_receive),
    }
    db.categories.insert_one(doc)
    return jsonify({'msg': '저장이 완료되었습니다!'})


@app.route('/study/<category>/update', methods=['POST'])
def study_update(category):
    percentage = int(request.form['percentage']) / 100
    db.categories.update_one({'category': category}, {'$inc': {'level': percentage}})
    return redirect('/study')


@app.route('/study/delete', methods=['POST'])
def study_delete():
    level_receive = request.form['level_give']
    db.categories.delete_one({'level': level_receive})
    return jsonify({'msg': '삭제가 완료되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
