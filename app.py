from flask import Flask, jsonify, request
from flask_restplus import Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

url = "https://www.scorebat.com/video-api/v1/"

@api.route('/api/items')
class Match(Resource):
    def get(self):
        try:
            r = requests.get(url)
            # print(r.status_code)
            data = json.loads(r.text)[:]

            proc_data = []
            for item in data:
                proc_data.append({'title':item['title'],'date':item['date'], 'team 1':item['side1']['name'], 'team 2':item['side2']['name'], 'league':item['competition']['name']})
            
            """
            The line: 'return jsonify(proc_data), 200' , will return in the console;

            TypeError: Object of type 'Response' is not JSON serializable

            Hence we use: 'return proc_data, 200' instead.
            """
            return proc_data, 200

        except KeyError:
            msg = {'Error message': 'Items cannot be found'}
            return msg,403

@api.route('/api/item/<int:id>')
class MatchById(Resource):
    def get(self, id):
        try:
            r = requests.get(url)
            # print(r.status_code)
            data = json.loads(r.text)[:]
            
            title = data[id]['title']
            date = data[id]['date']
            team_1 = data[id]['side1']['name']
            team_2 = data[id]['side2']['name']
            league = data[id]['competition']['name']

            msg = [{'title': title, 'date': date, 'team 1':team_1,'team 2':team_2,'league':league}]
            
            return msg, 200
        except IndexError:
            msg = {'Error message': 'Item cannot be found'}
            return msg,403

if __name__ == '__main__':
    app.run(debug=True)