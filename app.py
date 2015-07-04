#!flask/bin/python

from flask import Flask, jsonify, abort,make_response, request

app = Flask(__name__)

tasks = [
	{
		'id' : 1,
		'title' : u'Buy stuff',
		'desc' : 'Milk, Eggs, Bread, Sugar, Salt',
		'done' : False
	},
	{
		'id' : 2,
		'title' : u'Buy stuff 2',
		'desc' : 'Milk2, Eggs2, Bread2, Sugar2, Salt2',
		'done' : False
	}
]

@app.route('/')
def index():
	return "Hello!"

@app.route('/todo/api/v1.0/tasks/', methods = ['GET'])
def get_tasks():
	return jsonify({ 'tasks': tasks })

@app.route('/todo/api/v1.0/tasks/<int:id>', methods = ['GET'])
def get_task(id):
	task = [task for task in tasks if task['id'] == id ]
	if len(task) == 0:
		abort(404)
	else:
		return jsonify({ 'task': task[0] })

@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def add_task():
	if not request.json or not 'title' in request.json:
		abort(400)
	task = {
	'id' : tasks[-1]['id'] + 1,
	'title' : request.json['title'],
	'desc' : request.json.get('desc',""),
	'done' : False
	}
	tasks.append(task)
	return jsonify({ 'task' : task }), 201


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( {'error' : 'Not found'} ), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify( {'error' : 'Bad request'}), 400)

if __name__ == '__main__':
	app.run(debug = True)