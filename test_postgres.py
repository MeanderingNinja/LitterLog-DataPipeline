"""
Test connection to a local postgreSQL database to see if data is being stored properly
"""

import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="pa-test",
                                  password="pa-test",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="learning_alembic")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()

    print("PostgreSQL Server Information")
    print('--------------------------------------------------')
    print(connection.get_dsn_parameters())
    print(record)
    print('\n')

    # cursor.execute("DROP TABLE test_result")

    cursor.execute(("CREATE TABLE IF NOT EXISTS test_data ("
                    "id VARCHAR PRIMARY KEY,"
                    "operator VARCHAR UNIQUE,"
                    "station VARCHAR UNIQUE,"
                    "created_at VARCHAR UNIQUE,"
                    "test_duration VARCHAR UNIQUE,"
                    "config JSONB UNIQUE,"
                    "data JSONB UNIQUE"
                    ")"
                    ))

    cursor.execute(("CREATE TABLE IF NOT EXISTS test_results ("
                    "id VARCHAR PRIMARY KEY,"
                    "data_id VARCHAR UNIQUE,"
                    "created_at VARCHAR UNIQUE,"
                    "resource JSONB UNIQUE,"
                    "results JSONB UNIQUE"
                    ")"
                    ))
    print('Available Tables')
    print('--------------------------------------------------')
    cursor.execute("""SELECT table_name FROM information_schema.tables
           WHERE table_schema = 'public'""")
    for table in cursor.fetchall():
        print(table)

    print('\n')
    print('Information from each Table')
    print('--------------------------------------------------')
    cursor.execute('''SELECT * from test_data''')
    result = cursor.fetchall()
    print('test_data info')
    print(result)
    cursor.execute('''SELECT * from test_results''')
    result = cursor.fetchall()
    print('test_result_info')
    print(result)
    cursor.close()
    connection.commit()
    # cursor.execute(("CREATE TABLE test_data ();"))
    # cursor.fetchone()
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
except (Exception, Error) as error:

    print("Error while connecting to PostgreSQL", error)
