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

        elif "id" in data:
            db_helper.update_task_entry(task_id, data["id"], data["name"])
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


# @app.route("/search", methods=['POST','GET'])
# def search_comp():
#     """ returns rendered homepage """
#     comp = db_helper.search_list('AAP')
#     if request.method == 'POST':
#         data = request.get_json()
#         # print(data['text'])
#         comp = db_helper.search_list(data['text'])
#         # print(comp)
#     # if request.method == 'GET':
#     # return render_template("search.html", items=comp)
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(comp)

# @app.route("/search_page/<string:comp_id>")
# def search_page(comp_id):
#     """ returns rendered homepage """
#     # req = request.get_json()
#     # print(req)
#     # print(comp_id)
#     data = eval(comp_id)
#     # print(data)
#     # items = db_helper.fetch_todo()
#     # print(items)
#     return render_template("search.html", items=data)

@app.route("/search_page/<string:comp_id>")
def search_page(comp_id):
    """ returns rendered homepage """

    comp = db_helper.search_list(comp_id)

  
    return render_template("search.html", items=comp)

@app.route("/query_page")
def query_page():
    """ returns rendered homepage """

    comp = db_helper.query_list()

  
    return render_template("query1.html", items=comp)

@app.route("/query_page2")
def query_page2():
    """ returns rendered homepage """

    comp = db_helper.query_list2()

  
    return render_template("query2.html", items=comp)


@app.route("/")
def homepage():
    """ returns rendered homepage """

    items = db_helper.fetch_todo()
    # print(items)
    # print(1)
    return render_template("index.html", items=items)