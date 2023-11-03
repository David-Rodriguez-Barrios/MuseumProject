import mysql.connector

mydb = mysql.connector.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        password = '27Eggs@home')#Change to be your password

mycursor = mydb.cursor()

fd = open('museum_database.sql','r')
sqlFile = fd.read()
fd.close()
sqlCommands = sqlFile.split(';')

for command in sqlCommands:
        try:
                if command.strip() !='':
                        mycursor.execute(command)
        except IOError as msg:
                print('Command skipped: ', msg)
