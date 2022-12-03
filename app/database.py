"""Defines all the functions related to the database"""
from app._init_ import db
from datetime import date
from datetime import timedelta
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression

# def fetch_todo():
#     todo_list = [
#     {"id": 1, "task": "Task 1" , "status": "In Progress"},
#     {"id": 2, "task": "Task 2", "status": "Todo"},\
#     ]
#     return todo_list

def fetch_todo() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select * from Company;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[1],
            "task": result[2],
            "status": result[3]
        }
        todo_list.append(item)

    return todo_list

def fetch_user_list(userid: str):
    conn = db.connect()
    alllist=conn.execute("Select * from Company;").fetchall()
    query='Select CompanyId from CompaniesFollowed Where UserId="{}";'.format(userid)
    follow_results = conn.execute(query).fetchall()
    conn.close()
    follow_list=[]
    for f in follow_results:
        follow_list.append(f[0])
    todo_list = []
    for result in alllist:
        if (result[1]+'\r' in follow_list) or (result[1] in follow_list):
            item = {
                "id": result[1],
                "task": result[2],
                "status": "Unfollow"
            }
            todo_list.append(item)
        else:
            item = {
                "id": result[1],
                "task": result[2],
                "status": "Follow"
            }
            todo_list.append(item)

    return todo_list


def search_list(text: str) -> None:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    # query_results = conn.execute('Select * from Company where CompanyName LIKE  "%{}%" OR CompanyID LIkE  "%{}%" ;'.format(text, text)).fetchall()
    # query = 'Select * from Company where CompanyName LIKE "%%%s%%" OR CompanyID LIkE "%%%s%%"' % (text,text)
    # print(query)
    query_results = conn.execute('Select * from Company where CompanyName LIKE %s OR CompanyID LIKE %s LIMIT 10', ('%' + text + '%','%' + text + '%')).fetchall()
    # print(query_results)
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[1],
            "task": result[2],
            "status": result[3]
        }
        todo_list.append(item)
    print(todo_list)
    return todo_list

def search_user():
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    query_results = conn.execute('Select * from LoginInfo;').fetchall()
    #print(query_results)
    conn.close()
    user_list = {}
    for result in query_results:
        user_list[result[0]]=result[1]
    return user_list

def query_list() -> None:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    
    query = "SELECT UserId, sum FROM (SELECT sum(stock_change*StockPrice) sum, UserId FROM (SELECT ChangeInNumberOfStocks as stock_change, UserId, CompanyID FROM Purchase) a NATURAL JOIN StocksByDate GROUP BY UserId) b ORDER BY sum DESC, USERID LIMIT 15"
    # query_results = conn.execute('Select * from Company where CompanyName LIKE  "%{}%" OR CompanyID LIkE  "%{}%" ;'.format(text, text)).fetchall()
    # query = 'Select * from Company where CompanyName LIKE "%%%s%%" OR CompanyID LIkE "%%%s%%"' % (text,text)
    # print(query)
    query_results = conn.execute(query).fetchall()
    print(query_results)
    # print(query_results)
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            # "status": result[3]
        }
        todo_list.append(item)
    print(todo_list)
    return todo_list

def query_list2() -> None:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    
    query = "SELECT c.CompanyName, t.sum_, c.Followers FROM (SELECT SUM(pur.ChangeInPrice) as sum_, pur.CompanyID FROM Purchase pur GROUP BY CompanyID) as t NATURAL JOIN Company c WHERE (t.sum_) > 100000 ORDER BY t.sum_ DESC, c.Followers DESC LIMIT 15"
    # query_results = conn.execute('Select * from Company where CompanyName LIKE  "%{}%" OR CompanyID LIkE  "%{}%" ;'.format(text, text)).fetchall()
    # query = 'Select * from Company where CompanyName LIKE "%%%s%%" OR CompanyID LIkE "%%%s%%"' % (text,text)
    # print(query)
    query_results = conn.execute(query).fetchall()
    print(query_results)
    # print(query_results)
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)
    print(todo_list)
    return todo_list

def procedure() -> None:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    
    query = "Call updateprediction"
    # query_results = conn.execute('Select * from Company where CompanyName LIKE  "%{}%" OR CompanyID LIkE  "%{}%" ;'.format(text, text)).fetchall()
    # query = 'Select * from Company where CompanyName LIKE "%%%s%%" OR CompanyID LIkE "%%%s%%"' % (text,text)
    # print(query)
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "up": result[3]
        }
        todo_list.append(item)
    # print(todo_list)
    return todo_list
    

def update_task_entry(task_id: str, new_task_id: str, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """
    print(1)
    conn = db.connect()
    query1 = 'Update Company set CompanyName = "{}" where CompanyID = "{}";'.format(text, task_id)
    query2 = 'Update Company set CompanyID = "{}" where CompanyID = "{}";'.format(new_task_id, task_id)
    print(text)
    print(task_id)
    conn.execute(query1)
    conn.execute(query2)
    conn.close()


def update_status_entry(task_id: str, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """
    conn = db.connect()
    query = 'Update Company set Status = "{}" where CompanyID = "{}";'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_LoginInfo_database(userid: int,text: str,task_id:str):
    conn = db.connect()
    if text=="Follow":
        query = 'DELETE FROM CompaniesFollowed WHERE UserId="{}" AND CompanyId="{}";'.format(userid, task_id)
    elif text=="Unfollow":
        query = 'INSERT INTO CompaniesFollowed VALUES ("{}","{}");'.format(userid, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(id: str, name: str) ->  str:

    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()

    #last_id_q = conn.execute("Select LAST_INSERT_ID();")
    #last_id_q = [x for x in last_id_q]
    last_id_2 = conn.execute("Select max(id_num) from Company;").fetchall()
    #last_id = last_id_q[0][0]
    query = 'Insert Into Company (id_num, CompanyID, CompanyName, Status, Followers, CurrentStockPrice, CurrentGrowthRate, PredictedStockPrice, PredictedGrowthRate) VALUES ({}, "{}", "{}", "Follow", 0, 0, 0, 0, 0);'.format(
        int(last_id_2[0][0]) + 1, id, name)

    conn.execute(query)
    query = conn.execute("Select * from Company ORDER BY CompanyId;")
    #query_results = conn.execute("Select LAST_INSERT_ID();")
    #query_results = [x for x in query_results]
    conn.close()

    return id


def remove_task_by_id(task_id: str) -> None:
    """ remove entries based on task ID """

    conn = db.connect()
    query = 'Delete From Company where CompanyID="{}";'.format(task_id)
    conn.execute(query)
    conn.close()

# def userId(task_id: str)

# helper
def smart_comp_name(comp_name):
    cn_list = comp_name.split(' ')
    smart = ''
    if len(cn_list) >= 2:
        if cn_list[1] == 'Inc' or cn_list[1] == 'Inc.':
            smart = cn_list[0]
        else:
            smart = cn_list[0] + " " + cn_list[1]
    else:
        smart = cn_list[0]
    return smart
  

def refresh():
    conn = db.connect()
    query = 'select * from Company ;'
    result = conn.execute(query).fetchall()
    result = np.array(result)
    conn.close()

    # set up
    companies = pd.DataFrame(result) #import full data as dataframe
    companies = companies.sample(n=10, random_state=1) #sampling

    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1, requests_args={'verify':False})

    # emotion_list = ['accessible', 'pleasing', 'candid', 'agreeable', 'balanced']
    emotion_list = ['valuable', 'successful', 'candid', 'organic', 'steadfast', 'talented', 'unique', 'interesting', 'functional', 'educated', 
                'ready', 'credible', 'substantial', 'workable', 'perfect', 'possible', 'supreme', 'focused', 'maintainable', 'threatening']

    train_columns = ['CompanyID', 'Price'] + emotion_list + ['GrowthRate']
    train_set = pd.DataFrame([], columns=train_columns)
    predict_columns = ['CompanyID', 'Price'] + emotion_list
    predict_set = pd.DataFrame([], columns=predict_columns)

    # data making
    for index, company in companies.iterrows():
        smart_name = smart_comp_name(company['CompanyName'])
        search_list = ['"' + smart_name +  '" + "' + e + '"' for e in emotion_list]
        pytrends.build_payload(search_list, cat=0, timeframe="now 7-d", geo='US')
        trend = pytrends.interest_over_time()
        trend = trend.drop(['isPartial'], axis=1)
        trend = trend.resample('D').sum()
        stock = yf.download(company['CompanyID'], str(date.today() - timedelta(days = 7)), str(date.today()))
        # predict_set
        if date.today() - timedelta(days = 1) != stock.last('D').index.date:
            print("no stock price for new prediction")
            continue
        predict_insert = [company['CompanyID'], stock['Close'].last('D').values[0]] + trend.last('D').values.tolist()[0]
        predict_set.loc[len(predict_set)] = predict_insert

        trend = trend.drop(date.today())
        stock_reverse = stock.sort_index(ascending=False)
        for i, stock_row in stock_reverse.iterrows():
            try:
                next_stock_row = stock.iloc[[np.searchsorted(stock.index, i - timedelta(days = 1))]]
                next_trend = trend.loc[next_stock_row.index].squeeze()
                ns_price = next_stock_row['Close'].values[0]
                growth_rate = (stock_row['Close'] - ns_price) / ns_price
                if growth_rate == 0:
                    continue
                to_insert = [company['CompanyID'], ns_price] + next_trend.tolist() + [growth_rate]
                train_set.loc[len(train_set)] = to_insert
            except:
                break

    # model making and predict
    # generate regression dataset
    X = train_set.iloc[:, 1:len(list(train_set)) - 1].copy()
    y = train_set.iloc[:, len(list(train_set)) - 1].copy()
    # # fit final model
    model = LinearRegression()
    model.fit(X, y)
    # # new instances where we do not know the answer
    Xnew = predict_set.iloc[:, 1:].copy()
    # # make a prediction
    ynew = model.predict(Xnew)
    print(ynew)

    # output
    final_list = predict_set[['CompanyID', 'Price']]
    final_list['GrowthRate'] = ynew
    conn = db.connect()
        
    query_result1 = ""
    for i, list_row in final_list.iterrows():
        query = 'Update Company set PredictedGrowthRate = "{}" where CompanyID = "{}";'.format(list_row["GrowthRate"],list_row["CompanyID"])
        query2 = "SELECT CompanyID, PredictedGrowthRate from Company WHERE CompanyID = '{}'".format(list_row["CompanyID"])
        
        query_result1 = conn.execute(query2).fetchall()
        print(query_result1)
        conn.execute(query)
        query3= "SELECT CompanyID, PredictedGrowthRate from Company WHERE CompanyID = '{}'".format(list_row["CompanyID"])
        print(conn.execute(query3).fetchall())


    
    conn.close()