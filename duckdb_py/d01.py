# %%
# reference
# https://docs.python.org/3/library/sqlite3.html#sqlite3-tutorial
# https://duckdb.org/docs/api/python 
# https://docs.pola.rs/

import duckdb

# by default, duckdb creates an in-memory database
db = duckdb.connect()

# duck db can directly read csv files
# alternatively you can use `csv = db.read_csv('[file_path]')`
db.sql(""" 
select * from read_csv('./data/kaggle_employees.csv')
""")

# %%

# creating a duckdb table and callable variable
db.sql(""" 
CREATE OR REPLACE TABLE employees AS
       SELECT * FROM read_csv('./data/kaggle_employees.csv', header = True)
""")

print(db.table('employees'))

# %%

# this copy the employees table and create a file
db.execute("COPY employees TO './parq/employees.parquet' (FORMAT 'parquet')")

db.sql("select * from read_parquet('./parq/employees.parquet')")

db.sql("select * from employees")

# %%

# example queries

db.sql(""" 
select MAX("Bonus %") as max_bonus
from employees
""")

db.sql(''' 
select
       Salary,
       "Bonus %",
       ROUND(Salary + (Salary * ("Bonus %" / 100)),3) as total_salary
from employees
''')

db.sql('''
select
    Team,
    ROUND_EVEN(AVG(Salary), 3) as Avg_Salary
    from employees
    where Team is not NULL
    group by Team
    order by avg_salary desc
''')

db.sql(''' 
select
       Gender,
       CAST(AVG(Salary) AS int) as Avg_Salary,
       MAX(Salary)
    from employees
    where Gender is not NULL
    GROUP BY Gender
''')

db.sql('DROP TABLE employees')
db.sql('SHOW TABLES')


# %%
db.close()
#

# %%
