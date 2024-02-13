import sqlite3
import pandas as pd

con = sqlite3.connect("/opt/jupyterhub/jupyterhub.sqlite")
cur = con.cursor()

# Queries to list all the tables, info about tables such as column names, and query the tables
for row in cur.execute("""SELECT name FROM sqlite_master WHERE type='table';"""):print(row)
for row in cur.execute("""PRAGMA table_info('users')"""):print(row)
for row in cur.execute('select * from users;'):print(row)

# Query and print through Pandas as dataframe
df = pd.read_sql_query("select * from users;", con)
print(df)

