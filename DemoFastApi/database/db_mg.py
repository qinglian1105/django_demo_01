from dotenv import load_dotenv
import pymongo
import os


# Global variable
PWD = os.getcwd()
ENV_FILE_PATH = os.path.join(PWD, "initialize", ".env.develop")
load_dotenv(dotenv_path=ENV_FILE_PATH, override=True)
HOST = os.environ.get("MG_HOST")
USER = os.environ.get("MG_USERNAME")
PASSWORD = os.environ.get("MG_PASSWORD")
PORT = os.environ.get("MG_PORT")
CONN_STR = f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/?authSource=admin"
DB_NAME = "mydb"
TB_NAME = "credit_bureau"


# Connect to MongoDB
def mongo_connection():
    try:
        client = pymongo.MongoClient(CONN_STR)
        return client
    except Exception as e:
        print(e)


# Get default amount and count
def default_condition():
    try:
        m_client = mongo_connection()
        myclient = m_client
        mydb = myclient[DB_NAME]
        mycol = mydb[TB_NAME]
        pipeline = [
            {
                "$group": {
                    "_id": "$loan_status",
                    "count": {"$sum": 1},
                    "loan_amnt": {"$sum": "$loan_amnt"},
                }
            }
        ]
        docs = mycol.aggregate(pipeline)
        list_01 = []
        list_02 = []
        list_03 = []
        for doc in docs:
            if doc["_id"] in [1]:
                doc["_id"] = "Default"
            else:
                doc["_id"] = "Non-default"
            list_01.append(doc["_id"])
            list_02.append(doc["count"])
            list_03.append(doc["loan_amnt"])
        plist_01 = [
            {"name": list_01[0], "value": list_02[0]},
            {"name": list_01[1], "value": list_02[1]},
        ]
        plist_02 = [
            {"name": list_01[0], "value": list_03[0]},
            {"name": list_01[1], "value": list_03[1]},
        ]
        dict = {"count": plist_01, "loan_amnt": plist_02}
        return dict
    except Exception as e:
        raise e
    finally:
        myclient.close()


# Get default condition by age, amount and count
def default_condition_age():
    try:
        m_client = mongo_connection()
        myclient = m_client
        mydb = myclient[DB_NAME]
        mycol = mydb[TB_NAME]
        pipeline = [
            {"$match": {"person_age": {"$lt": 100}}},
            {
                "$group": {
                    "_id": "$person_age",
                    "count": {"$sum": 1},
                    "loan_amnt": {"$sum": "$loan_amnt"},
                    "person_income": {"$sum": "$person_income"},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        docs = mycol.aggregate(pipeline)
        list_age = []
        list_count = []
        list_loan = []
        list_income = []
        for doc in docs:
            list_age.append(str(doc["_id"]))
            list_count.append(doc["count"])
            list_loan.append(round(doc["loan_amnt"] / 1000000, 2))
            list_income.append(round(doc["person_income"] / 1000000, 2))
        dict = {
            "age": list_age,
            "count": list_count,
            "loan": list_loan,
            "income": list_income,
        }
        return dict
    except Exception as e:
        raise e
    finally:
        myclient.close()


# Get DB information
def get_mongodb_info():
    try:
        m_client = mongo_connection()
        m_db = m_client[DB_NAME]
        collections = m_db.list_collection_names(session=None)
        outputs = []
        for coll in collections:
            output = dict()
            output["db_name"] = DB_NAME
            output["collection_name"] = coll
            outputs.append(output)
        return outputs
    except Exception as e:
        raise e
    finally:
        m_client.close()
