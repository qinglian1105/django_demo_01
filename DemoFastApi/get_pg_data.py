import psycopg2
import pandas as pd


host = 'your_host'
dbname = 'your_dbname'
user = 'your_username'
password = 'your_password'
port = 'your_port'


def get_connection(host, dbname, user, password, port):
    conn = psycopg2.connect(database=dbname, user=user, 
                            password=password, host=host, 
                            port=port)        
    return conn


def get_html_table(dss):
    df = pd.DataFrame(dss)  
    res = df.to_html()  
    res = res.replace('<table border="1" class="dataframe">','<table class="table table-striped">')
    res = res.replace('<thead>','<thead class="success">')
    res = res.replace('<tr style="text-align: right;">','<tr>')    
    res = res.replace('<td>','<td class="text-end" style="border: 1px; text-align: center;">')
    res = res.replace('<th></th>','<th style="border: 1px; text-align: center;">Num</th>')
    res = res.replace('<th>','<th style="border: 1px; text-align: center;">')    
    return {"tb": res}


def get_all_years():      
    try:        
        conn = get_connection(host, dbname, user, password, port)
        cursor = conn.cursor()        
        sql_str = f"""SELECT distinct(right(issue_d,4)) as yyyy FROM lendingclub
                      WHERE issue_d is not NULL ORDER BY right(issue_d,4) desc;"""
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
        conn = get_connection(host, dbname, user, password, port)
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
        conn = get_connection(host, dbname, user, password, port)
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
        conn = get_connection(host, dbname, user, password, port)
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
        conn = get_connection(host, dbname, user, password, port)
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
        conn = get_connection(host, dbname, user, password, port)
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
        dss = {"mm":ds01, "amt":ds02}    
        return dss             
    except Exception as e:
        raise e
    finally:    
        cursor.close()
        conn.close()        
   

def get_month_count(year):
    try:
        conn = get_connection(host, dbname, user, password, port)
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
        dss = {"mm":ds01, "count":ds02}    
        return dss             
    except Exception as e:
        raise e
    finally:    
        cursor.close()
        conn.close() 


def get_purpose(year):
    try:
        conn = get_connection(host, dbname, user, password, port)
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
                ds['Purpose'] = row[0]
                ds['Counts'] = f"{row[1]:,}"
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
        conn = get_connection(host, dbname, user, password, port)
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
                ds['Occupation'] = row[0]
                ds['Counts'] = f"{row[1]:,}"
                dss.append(ds) 
            i = i + 1          
        return get_html_table(dss)               
    except Exception as e:
        raise e
    finally:    
        cursor.close()
        conn.close()        
    