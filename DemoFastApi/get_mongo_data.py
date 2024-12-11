import pymongo


# Global variables
host = 'your_host'
port = 'your_port'
username = 'your_username'
password = 'your_password'
db_name = 'your_dbname'
tb_name = 'your_table_name'


# Get connection to mongodb
def get_mongo_connection(host, port, username, password):
    m_client = pymongo.MongoClient(host = host,
                                   port = port,  
                                   username = username,
                                   password = password)    
    return m_client


# Get default amount and count
def default_condition():
    try:
        m_client = get_mongo_connection(host, port, username, password)
        myclient = m_client
        mydb = myclient[db_name]
        mycol = mydb[tb_name]
        pipeline = [{'$group': {'_id': '$loan_status', 
                                'count': {'$sum': 1},
                                'loan_amnt': {'$sum': '$loan_amnt'} 
                               }
                    }]
        docs = mycol.aggregate(pipeline)  
        list_01 = []
        list_02 = []
        list_03 = []
        for doc in docs: 
            if doc['_id'] in [1]:
                doc['_id'] = "Default"
            else:
                doc['_id'] = "Non-default"  
            list_01.append(doc['_id'])
            list_02.append(doc['count'])  
            list_03.append(doc['loan_amnt'])            
        plist_01=[{'name':list_01[0], 'value':list_02[0]},
                {'name':list_01[1], 'value':list_02[1]}]
        plist_02=[{'name':list_01[0], 'value':list_03[0]},
                {'name':list_01[1], 'value':list_03[1]}]
        dict = {'count': plist_01, 'loan_amnt': plist_02}
        return dict
    except Exception as e:
        raise e
    finally:          
        myclient.close()


# Get default condition by age, amount and count
def default_condition_age():
    try:
        m_client = get_mongo_connection(host, port, username, password)
        myclient = m_client
        mydb = myclient[db_name]
        mycol = mydb[tb_name]
        pipeline = [{'$match': { 'person_age': {'$lt': 100} }},
                    {'$group': {'_id': '$person_age', 
                                'count': {'$sum': 1},
                                'loan_amnt': {'$sum': '$loan_amnt'}, 
                                'person_income': {'$sum': '$person_income'},                      
                                }},
                    {'$sort': {'_id': 1}},]  
        docs = mycol.aggregate(pipeline)          
        list_age = []
        list_count = []
        list_loan = []
        list_income = []
        for doc in docs:            
            list_age.append(str(doc['_id']))
            list_count.append(doc['count'])
            list_loan.append(round(doc['loan_amnt']/1000000,2))
            list_income.append(round(doc['person_income']/1000000,2)) 
        dict = {'age': list_age, 'count': list_count, 
                'loan': list_loan, 'income': list_income}        
        return dict
    except Exception as e:
        raise e
    finally:          
        myclient.close()
  
