from flask import Flask, jsonify, request
from flask_restplus import Resource, Api, fields
import requests
import json

app = Flask(__name__)
api = Api(app=app, version = "1.0", title = "Soccer API", description = "Fetches matches recent matches from score bat and displays them")

name_space = api.namespace('api', description='Main APIs')




url = "https://www.scorebat.com/video-api/v1/"

@name_space.route('/items')
class Match(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
    def get(self):
        try:

            r = requests.get(url)
            # print(r.status_code)
            data = json.loads(r.text)[:]

            proc_data = []
            for item in data:
                proc_data.append({'title':item['title'],'date':item['date'], 'team 1':item['side1']['name'], 'team 2':item['side2']['name'], 'league':item['competition']['name']})

            output_data = {
				"status": "Matches retrieved",
				"Matches" : proc_data
			}
            """
            The line: 'return jsonify(data), 200' , will return in the console;

            TypeError: Object of type 'Response' is not JSON serializable

            Hence we use: 'return data, 200' instead for those not using the @api.doc decorator, or just return data while using the decorator.
            """
            return output_data

        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")
    

@name_space.route('/item/<int:id>')
class MatchById(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, params={ 'id': 'Specify the Id associated with the match' })
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

            match = [{'title': title, 'date': date, 'team 1':team_1,'team 2':team_2,'league':league}]

            output_data = {
				"status": "Match retrieved",
				"Match" : match
			}
            
            return output_data

        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

if __name__ == '__main__':
    app.run(debug=True)