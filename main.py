from app._init_ import app
from flask import session, g
from app import database as db_helper


@app.before_request
def my_before_request():
    userid = session.get("userid")
    if userid:
        user = db_helper.search_user(userid)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
    return {"user": g.user}

if __name__ == '__main__':
    
    app.run(debug=True)