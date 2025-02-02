from dotenv import load_dotenv
import pandas as pd
import psycopg2
import os


# Global variable
DBS = ["tst", "fastapi_tst"]
DB_INFO_COLS = [
    "schema",
    "table",
    "total_size",
    "data_size",
    "index_size",
    "rows",
    "total_row_size",
    "row_size",
]
PWD = os.getcwd()
ENV_FILE_PATH = os.path.join(PWD, "initialize", ".env.develop")
load_dotenv(dotenv_path=ENV_FILE_PATH, override=True)
HOST = os.environ.get("PG_HOST")
USER = os.environ.get("PG_USER")
PASSWORD = os.environ.get("PG_PASSWORD")
PORT = os.environ.get("PG_PORT")
CONN_STR = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}"
          
          
# Connect to DB
def pg_connection(db_name="tst"):
    try:               
        conn = psycopg2.connect(f"{CONN_STR}/{db_name}")        
        return conn
    except Exception as e:
        print(e)


# Transfer dataframe into html table
def get_html_table(dss):
    try:
        df = pd.DataFrame(dss)
        res = df.to_html()
        res = res.replace(
            '<table border="1" class="dataframe">',
            '<table class="table table-striped">',
        )
        res = res.replace("<thead>", '<thead class="success">')
        res = res.replace('<tr style="text-align: right;">', "<tr>")
        res = res.replace(
            "<td>", '<td class="text-end" style="border: 1px; text-align: center;">'
        )
        res = res.replace(
            "<th></th>", '<th style="border: 1px; text-align: center;">Num</th>'
        )
        res = res.replace("<th>", '<th style="border: 1px; text-align: center;">')
    except Exception as e:
        print(e)
    return {"tb": res}


def get_all_years():
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = "SELECT distinct(right(issue_d,4)) as yyyy FROM lendingclub \
                   WHERE issue_d is not NULL ORDER BY right(issue_d,4) desc;"
        cursor.execute(sql_str)
        years = []
        rows = cursor.fetchall()
        for row in rows:
            years.append(row[0])
        dss = years[0:5]
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_loan_amt(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT sum(loan_amnt) as total_loan FROM lendingclub 
                      WHERE right(issue_d,4)='{year}';"""
        cursor.execute(sql_str)
        row = cursor.fetchone()
        dss = {"total_loan": round(row[0])}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_loan_count(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT count(loan_amnt) as total_count FROM lendingclub 
                      WHERE right(issue_d,4)='{year}';"""
        cursor.execute(sql_str)
        row = cursor.fetchone()
        dss = {"total_count": round(row[0])}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_default_amt(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT sum(loan_amnt) as default_amt FROM lendingclub 
                      WHERE right(issue_d,4)='{year}' and 
                            loan_status in ('Default','Charged Off');"""
        cursor.execute(sql_str)
        row = cursor.fetchone()
        dss = {"default_amt": round(row[0])}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_default_count(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT count(loan_amnt) as default_count FROM lendingclub 
                      WHERE right(issue_d,4)='{year}' and 
                            loan_status in ('Default','Charged Off');"""
        cursor.execute(sql_str)
        row = cursor.fetchone()
        dss = {"default_count": round(row[0])}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_month_loan(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""
        SELECT issue_d, left(issue_d,3) as mm,
            case 
                when left(issue_d,3)='Jan' then 1
                when left(issue_d,3)='Feb' then 2
                when left(issue_d,3)='Mar' then 3
                when left(issue_d,3)='Apr' then 4
                when left(issue_d,3)='May' then 5
                when left(issue_d,3)='Jun' then 6
                when left(issue_d,3)='Jul' then 7
                when left(issue_d,3)='Aug' then 8
                when left(issue_d,3)='Sep' then 9
                when left(issue_d,3)='Oct' then 10
                when left(issue_d,3)='Nov' then 11
            else 12 
            end as mm
            ,sum(loan_amnt) as month_loan FROM lendingclub 
            WHERE right(issue_d,4)='{year}' 
            GROUP BY issue_d ORDER BY
            (case 
                when left(issue_d,3)='Jan' then 1
                when left(issue_d,3)='Feb' then 2
                when left(issue_d,3)='Mar' then 3
                when left(issue_d,3)='Apr' then 4
                when left(issue_d,3)='May' then 5
                when left(issue_d,3)='Jun' then 6
                when left(issue_d,3)='Jul' then 7
                when left(issue_d,3)='Aug' then 8
                when left(issue_d,3)='Sep' then 9
                when left(issue_d,3)='Oct' then 10
                when left(issue_d,3)='Nov' then 11
            else 12 
            end) asc;"""
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        ds01 = []
        ds02 = []
        for row in rows:
            ds01.append(row[1])
            ds02.append(row[3])
        dss = {"mm": ds01, "amt": ds02}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_month_count(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""
        SELECT issue_d, left(issue_d,3) as mm,
            case 
                when left(issue_d,3)='Jan' then 1
                when left(issue_d,3)='Feb' then 2
                when left(issue_d,3)='Mar' then 3
                when left(issue_d,3)='Apr' then 4
                when left(issue_d,3)='May' then 5
                when left(issue_d,3)='Jun' then 6
                when left(issue_d,3)='Jul' then 7
                when left(issue_d,3)='Aug' then 8
                when left(issue_d,3)='Sep' then 9
                when left(issue_d,3)='Oct' then 10
                when left(issue_d,3)='Nov' then 11
            else 12 
            end as mm
            ,count(loan_amnt) as month_count FROM lendingclub 
            WHERE right(issue_d,4)='{year}' 
            GROUP BY issue_d ORDER BY
            (case 
                when left(issue_d,3)='Jan' then 1
                when left(issue_d,3)='Feb' then 2
                when left(issue_d,3)='Mar' then 3
                when left(issue_d,3)='Apr' then 4
                when left(issue_d,3)='May' then 5
                when left(issue_d,3)='Jun' then 6
                when left(issue_d,3)='Jul' then 7
                when left(issue_d,3)='Aug' then 8
                when left(issue_d,3)='Sep' then 9
                when left(issue_d,3)='Oct' then 10
                when left(issue_d,3)='Nov' then 11
            else 12 
            end) asc;"""
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        ds01 = []
        ds02 = []
        for row in rows:
            ds01.append(row[1])
            ds02.append(row[3])
        dss = {"mm": ds01, "count": ds02}
        return dss
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_purpose(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT purpose, count(purpose) as total_count FROM lendingclub 
                      WHERE right(issue_d,4)='{year}' 
                      GROUP BY purpose ORDER BY count(purpose) desc;"""
        cursor.execute(sql_str)
        dss = []
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            if i < 10:
                ds = {}
                ds["Purpose"] = row[0]
                ds["Counts"] = f"{row[1]:,}"
                dss.append(ds)
            i = i + 1
        return get_html_table(dss)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_occupation(year):
    try:
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f"""SELECT emp_title as occupation, count(emp_title) as total_count FROM lendingclub 
                      WHERE right(issue_d,4)='{year}' 
                      GROUP BY emp_title ORDER BY count(emp_title) desc;"""
        cursor.execute(sql_str)
        dss = []
        rows = cursor.fetchall()
        i = 0
        for row in rows:
            if i < 10:
                ds = {}
                ds["Occupation"] = row[0]
                ds["Counts"] = f"{row[1]:,}"
                dss.append(ds)
            i = i + 1
        return get_html_table(dss)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


# Get DB information
def get_pg_db_info():
    try:
        cols = DB_INFO_COLS
        conn = pg_connection()
        cursor = conn.cursor()
        sql_str = f""" 
                SELECT
                nspname AS {cols[0]},
                pg_class.relname AS {cols[1]},
                pg_size_pretty(pg_total_relation_size(pg_class.oid)) AS {cols[2]},
                pg_size_pretty(pg_relation_size(pg_class.oid)) AS {cols[3]},
                pg_size_pretty(pg_indexes_size(pg_class.oid)) AS {cols[4]},
                pg_stat_user_tables.n_live_tup AS {cols[5]},
                pg_size_pretty(
                    pg_total_relation_size(pg_class.oid) / 
                    (pg_stat_user_tables.n_live_tup + 1)
                ) AS {cols[6]},
                pg_size_pretty(
                    pg_relation_size(pg_class.oid) / 
                    (pg_stat_user_tables.n_live_tup + 1)
                ) AS {cols[7]}
                FROM pg_stat_user_tables JOIN pg_class
                ON pg_stat_user_tables.relid = pg_class.oid
                JOIN pg_catalog.pg_namespace AS ns
                ON pg_class.relnamespace = ns.oid
                ORDER BY pg_total_relation_size(pg_class.oid) DESC;
                """
        cursor.execute(sql_str)
        infos = []
        rows = cursor.fetchall()
        for row in rows:
            dict_row = dict()
            for i, j in zip(cols, row):
                dict_row[i] = j
            infos.append(dict_row)
        return infos
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def pgdb_user():
    try:
        conn = pg_connection(DBS[1])        
        cursor = conn.cursor()
        sql_str = "SELECT * FROM api_user_table;"
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        records = dict()
        for row in rows:
            record = dict()
            record["username"] = row[1]
            record["hashed_password"] = row[2]
            records[row[1]] = record
            return records
    except Exception as e:
        print(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
