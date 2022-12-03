""" Specifies routing for the application"""
from flask import render_template, request, jsonify, redirect, url_for, session, g
# from werkzeug.security import check_password_hash
from app._init_ import app
from app import database as db_helper


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user = db_helper.search_user()
        #if userid != user[0] or password != user[1]:
        #if check_password_hash(user[1], password):
        #    session['userid'] = user[0]
        if not userid in user.keys():
            error = 'Invalid User ID. Please try again.'
            return render_template('login.html', error=error)
        if password == user[userid]:
            session['userid'] = userid
            return redirect(url_for('homepage'))
        else:
            error = 'Invalid Password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('homepage'))

# @app.route('/account', methods=['GET', 'POST'])
# def account():

#     return render_template('account.html')

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
    userid=session.get("userid")
    
    try:
        if "status" in data:
            if userid:
                db_helper.update_LoginInfo_database(userid,data["status"],task_id)
                return redirect(url_for('user_homepage',x=userid))
            else:
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

@app.route("/procedure_page")
def procedure_():
    """ returns rendered procedure_page """

    comp = db_helper.procedure()
    print(comp)

  
    return render_template("procedure.html", items=comp)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    # items=db_helper.fetch_todo()
    if g.user != None:
        items = db_helper.fetch_user_list(g.user)
    else:
        items = db_helper.fetch_todo()

    return render_template("index.html", items=items)

@app.route("/refresh/", methods=['POST'])
def refresh():
    db_helper.refresh()
    print("Successfully refresh")
    return redirect(url_for('homepage'))

# @app.route("/user_homepage",methods=['GET','POST'])
# def user_homepage():
#     """ returns rendered homepage """
#     y=request.args.get('x')
#     items = db_helper.fetch_user_list(y)
#     return render_template("index.html", items=items)

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