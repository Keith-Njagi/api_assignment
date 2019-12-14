from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

url = "https://www.scorebat.com/video-api/v1/"
r = requests.get(url)

@app.route('/api')
def matches():
    print(r.status_code)
    data = json.loads(r.text)[:]

    proc_data = []

    for item in data:
        proc_data.append({'title':item['title'],'date':item['date'], 'team 1':item['side1']['name'], 'team 2':item['side2']['name'], 'league':item['competition']['name']})
    #print(proc_data)

    return jsonify(proc_data), 200

@app.route('/api/<int:id>')
def matches_per_id(id):
    print(r.status_code)
    data = json.loads(r.text)[:]
    
    title = data[id]['title']
    date = data[id]['date']
    team_1 = data[id]['side1']['name']
    team_2 = data[id]['side2']['name']
    league = data[id]['competition']['name']

    #print(title,', ', date, ', ', team_1, ', ', team_2, ', ', league)
    msg = [{'title': title, 'date': date, 'team 1':team_1,'team 2':team_2,'league':league}]

    
    return jsonify(msg), 200


if __name__ == '__main__':
    app.run(debug=True)