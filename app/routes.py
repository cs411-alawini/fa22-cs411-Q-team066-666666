""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app._init_ import app
from app import database as db_helper


@app.route("/delete/<string:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """
    # print(1)
    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<string:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()


    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}

        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
            print(task_id)
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)



@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    print("called create")
    data = request.get_json()
    print(data['id'])
    db_helper.insert_new_task(data['id'], data['name'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items)