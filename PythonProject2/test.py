import pypyodbc as odbc
driver_name = 'SQL Server'
server_name = 'DESKTOP-FF9UBA0'
database_name = 'adventureworks'

connection_string = f"""Driver={driver_name};
                        Server={server_name};
                        Database={database_name};
                        Trust_Connection = yes;
                        """
conn = odbc.connect(connection_string)
print(conn)
