import mysql.connector
from tabulate import tabulate

def inputChecker(text, dataType, varcharLen = 50, canBeNull = True):
    DataTypeForm = {'integer':'value','float':'value','string': f'with length {varcharLen}','date':'in the form of "YYYY-MM-DD"'}
    while (True):
        print(text)
        print(f'input must be a {dataType} {DataTypeForm[dataType]}')
        userInput = input()
        if (not canBeNull and userInput in ['',' ', None]):
            print('Value can not be None, '' or ' '. Please try again')
            continue
        if (dataType == 'integer' and (userInput.isdigit() == False and userInput != '' and userInput != None)):
            print('Not a proper integer. Please try again')
        elif (dataType == 'float' and (userInput.replace('.','').isdigit() == False and userInput != '' and userInput != None)):
            print('Not a proper float. Please try again')
        elif (dataType == 'string' and (len(userInput) > varcharLen and userInput != '' and userInput != None)):
            print(f'String length is too long it should be up to {varcharLen} characters long. please try again')
        elif (dataType == 'date' and ((999 < int(userInput.split('-')[0]) < 10000 and 0 < int(userInput.split('-')[1]) < 13 and 0 < int(userInput.split('-')[2]) < 32) and userInput != '' and userInput != None)):
            print('invalid date. should be a proper date in the form "YYYY-MM-DD". Please try again')
        else: return userInput

def SearchSelection(mycursor):
    attributes = {
    'ART_OBJECT':[['Id_no', 'integer'], ['Title', 'string'], ['Year', 'integer'], ['Description', 'string'], ['Epoch', 'string'], ['COO', 'string'], ['Artist', 'string']],
    'ARTIST':[['Name', 'string'], ['Description', 'string'], ['Main_style', 'string'], ['Date_died', 'integer'], ['Date_born', 'integer'], ['Epoch', 'string'], ['COO', 'string']],
    'EXHIBITIONS':[['Name', 'string'], ['Start_date', 'date'], ['End_date', 'date']],
    'COLLECTIONS':[['Name', 'string'], ['Address', 'string'], ['Type', 'string'], ['Contact_person', 'string'], ['Description', 'string'], ['Phone', 'string']],
    'PAINTING':[['Id_no', 'integer'], ['Drawn_on', 'string'], ['Paint_type', 'string'], ['Style', 'string']],
    'SCULPTURE_STATUE':[['Id_no', 'integer'], ['Weight', 'float'], ['Material', 'string'], ['Style', 'string'], ['Height', 'float']],
    'OTHER':[['Id_no', 'integer'], ['Style', 'string'], ['Type', 'string']],
    'BORROWED':[['Id_no', 'integer'], ['Date_borrowed', 'date'], ['Date_returned', 'date'], ['Collection_N', 'string']],
    'PERMANENT_C':[['Id_no', 'integer'], ['Date_acquired', 'date'], ['Cost', 'float'], ['Status', 'string']],
    'DISPLAYED_IN':[['Id_no','integer'],['Name','string']]
    }

    print("What are you looking for?")
    print("1. Artists")
    print("2. Art Object")
    print("3. Collections")
    print("4. Exhibitions")
    print("5. Borrowed art")
    print("6. Permanent art")
    print("7. More Sculpture/Statue information")
    print("8. More Painting information")
    print("9. Other specific art object information")
    print("10. Where art objects are displayed")
    print("11. if you would like to cancel the search")
    selection = input("")

    choice = {'1':'ARTIST','2':'ART_OBJECT','3':'COLLECTIONS','4':'EXHIBITIONS','5':'BORROWED','6':'PERMANENT_C','7':'SCULPTURE_STATUE','8':'PAINTING','9':'OTHER','10':'DISPLAYED_IN'}
    while(True):
        if (selection in ['1','2','3','4','5','6','7','8','9','10','11']):
            if (selection == '11'): return
            value = choice[selection]
            break
        else: selection = input("Please input a valid option: ")
    a=input("If you would like to see all the information in " + value + " enter: 0, if you would like to search with an attribute, enter: 1 ")
    if a=='0':
        instr= " SELECT * FROM "+ value
    else:
        print("Which attribute would you like to search through? ")
        i=0
        for x in attributes[value]:
            i+=1
            print(f'{i}. {x[0]}')
        attribute_selection=input("Input the number corresponding to the attribute, if you would like to quit input 11:")
        while(True):
            if(attribute_selection.isdigit() == True):
                if(int(attribute_selection) in range(1,i+1)):
                    break
                else:   attribute_selection = input("Please input a valid option: ")
            else:   attribute_selection = input("Please input a valid option: ")
    
        search_key_attribute=inputChecker("Input the attribute value ",attributes[value][int(attribute_selection)-1][1],varcharLen = 300,canBeNull = False)
        if attributes[value][int(attribute_selection)-1][1] in ['integer','float']:
            instr= "SELECT * fFROMrom " + value + " WHERE " + attributes[value][int(attribute_selection)-1][0] + ' = '+search_key_attribute
        else: 
            instr = "SELECT * FROM "+ value+" WHERE "+ attributes[value][int(attribute_selection)-1][0] + " = '"+search_key_attribute+"'"
        while (True):
            multi=input("Would you like to search with through additional attribute: Yes or No")
    
            if multi in ['n','N','no','No']:
                break
            elif multi in ['y','Y','yes','Yes']:
                attribute_selection=input("Input the number corresponding to the attribute")
                while(True):
                    if(attribute_selection.isdigit() == True):
                        if(int(attribute_selection) in range(1,i+1)):
                            break
                        else:   attribute_selection = input("Please input a valid option: ")
                    else:   attribute_selection = input("Please input a valid option: ")
                
                search_key_attribute=inputChecker("Input the attribute value ",attributes[value][int(attribute_selection)-1][1],varcharLen = 300,canBeNull = False)
                
                if attributes[value][int(attribute_selection)-1][1] in ['integer','float']:
                    instr= instr+' AND ' +attributes[value][int(attribute_selection)-1][0] + ' = '+search_key_attribute
                else: 
                    instr = instr +' AND ' +attributes[value][int(attribute_selection)-1][0] + " = '"+search_key_attribute+"'"
    try:
        mycursor.execute(instr)
        col_names=mycursor.column_names
        search_result=mycursor.fetchall()
        data=[col_names]
        for x in search_result:
            data.append(x)
        print(tabulate(data,tablefmt='grid'))
        
         
        print()

    except: 
        print('Command could not be executed')
    return  

def insertData(mydb, mycursor):
    while(True):
        print ('Where would you like to insert data?:\n1 - Art_Object\n2 - Artist\n3 - Exhibition\n4 - Collection\n5 - Displayed_in\n6 - exit')
        userInput = input('please input 1, 2, 3, 4, 5 or 6: ')

        #Art_Object 
        if (userInput == '1'):
            Id_no = inputChecker('What is the art object\'s ID?  ', 'integer', canBeNull = False)
            Title = inputChecker('What is the art object\'s Title?  ','string')
            Year = inputChecker('What year is the art object from?  ','integer')
            Description = inputChecker('What is the description of the art object?  ','string',varcharLen = 300)
            Epoch = inputChecker('What Epoch is the art object from?  ','string')
            COO = inputChecker('What is the country of origin of this art object?  ','string')
            Artist = inputChecker('What is the Art objects ID?  ','string',canBeNull = False)
            try:
                mycursor.execute(f'INSERT INTO ART_OBJECT VALUES ({Id_no}, "{Title}", {Year}, "{Description}", "{Epoch}", "{COO}", "{Artist}");')
                mydb.commit()
            except: 
                print('Command could not be executed')

            
            while(True):
                print ('What type of art is this object?:\n1 - Painting\n2 - Sculpture/Statue\n3 - Others')
                nextInput = input('please input 1, 2, or 3: ')

                #Painting
                if (nextInput == '1'):
                    Drawn_on = inputChecker('What is the painting drawn on?  ','string')
                    Paint_type = inputChecker('What is the painting painted with?  ','string')
                    Style = inputChecker('What is the painting\'s style?  ','string')
                    try:
                        mycursor.execute(f'INSERT INTO PAINTING VALUES ({Id_no}, "{Drawn_on}", "{Paint_type}","{Style}");')
                        mydb.commit()
                    except: 
                        print('Command could not be executed')
                    break

                #Sculpture/Statue
                elif (nextInput == '2'):
                    Weight = inputChecker('What is the sculpture/statue\'s weight?  ','float')
                    Material = inputChecker('What is the sculpture/statue made of?  ','string')
                    Style = inputChecker('What is the sculpture/statue\' style?  ','string')
                    Height = inputChecker('What is the sculpture/statue\' height?  ','float')
                    try:
                        mycursor.execute(f'INSERT INTO SCULPTURE_STATUE VALUES ({Id_no}, {Weight}, "{Material}","{Style}",{Height});')
                        mydb.commit()
                    except IOError as msg: 
                        print('Command skipped: ', msg)
                    break

                #Others
                elif (nextInput == '3'):
                    Style = inputChecker('What is the object\'s style?  ','string')
                    Type = inputChecker('What is the object\'s type?  ','string')
                    try:
                        mycursor.execute(f'INSERT INTO OTHER VALUES ({Id_no}, "{Style}", "{Type}");')
                        mydb.commit()
                    except IOError as msg: 
                        print('Command skipped: ', msg)
                    break
                else: print('Not a valid input, please try again')
            
            while(True):

                print ('Is this piece of art borrowed or from a permanent collection?:\n1 - Borrowed\n2 - Permanent Collection')
                nextInput = input('please input 1 or 2: ')

                #Borrowed
                if (nextInput == '1'):
                    Date_borrowed = inputChecker('What date was this art piece borrowed on?  ','date')
                    Date_returned = inputChecker('What date will the art piece be returned?  ','date')
                    Collection_N = inputChecker('What collection is this art piece from?  ','string',varcharLen = 15)
                    try:
                        mycursor.execute(f'INSERT INTO BORROWED VALUES ({Id_no}, "{Date_borrowed}", "{Date_returned}","{Collection_N}");')
                        mydb.commit()
                    except IOError as msg: 
                        print('Command skipped: ', msg)
                    break

                #Permanent Collection
                elif (nextInput == '2'):
                    Date_acquired = inputChecker('What date was this art piece acquired on?  ','date')
                    Cost = inputChecker('What is the cost of this art piece?  ','float')
                    Status = inputChecker('What is the status of this art piece?  ','string',varcharLen = 15)
                    try:
                        mycursor.execute(f'INSERT INTO PERMANENT_C VALUES ({Id_no}, "{Date_acquired}", {Cost},"{Status}");')
                        mydb.commit()
                    except IOError as msg: 
                        print('Command skipped: ', msg)
                    break

                else: print('Not a valid input, please try again')

            break

        #Artist
        elif (userInput == '2'):
            Name = inputChecker('What is the name of the artist  ','string',canBeNull = False)
            Description = inputChecker('What is the description of the artist?  ','string',varcharLen = 300)
            Main_style = inputChecker('What isa this artist\'s main style?  ','string')
            Date_died = inputChecker('What is the date that this artist died?  ','integer')
            Date_born = inputChecker('What is the date that this artist was born?  ','integer')
            Epoch = inputChecker('what epoch is this artist from?  ','string')
            COO = inputChecker('What is this artist\'s country of origin?  ','string')
            try:
                mycursor.execute(f'INSERT INTO ARTIST VALUES ("{Name}", "{Description}", "{Main_style}", {Date_died}, {Date_born}, "{Epoch}", "{COO}");')
                mydb.commit()
            except: 
                print('Command could not be executed')
            break

        #Exhibition
        elif (userInput == '3'):
            Name = inputChecker('What is the name of the exhibition?  ','string',canBeNull = False)
            Start_date = inputChecker('what is the exhibition\'s start date?  ','date')
            End_date = inputChecker('what is the exhibition\'s end date?  ','date')
            try:
                mycursor.execute(f'INSERT INTO EXHIBITIONS VALUES ("{Name}", "{Start_date}", "{End_date}");')
                mydb.commit()
            except: 
                print('Command could not be executed')
            break

        #Collection
        elif (userInput == '4'):

            Name = inputChecker('What is the name of the collection?  ','string',varcharLen = 15,canBeNull = False)
            Address = inputChecker('What is the collection\'s address?  ','string')
            Type = inputChecker('What is the collection\'s type?  ','string',varcharLen = 15)
            Contact_person = inputChecker('Who is the is the collection\'s contact person?  ','string',varcharLen = 30)
            Description = inputChecker('What is a description of this collection?  ','string',varcharLen = 300)
            Phone = inputChecker('What is a phone number to the collection?  ','string',varcharLen = 15)
            try:
                mycursor.execute(f'INSERT INTO COLLECTIONS VALUES ("{Name}", "{Address}", "{Type}","{Contact_person}","{Description}","{Phone}");')
                mydb.commit()
            except: 
                print('Command could not be executed')
            break

        elif (userInput == '5'):

            Id_no = inputChecker('What is the art object\'s ID?  ', 'integer', canBeNull = False)
            Name = inputChecker('What is the name of the exhibition the art object is displayed in?  ','string',canBeNull = False)
            try:
                mycursor.execute(f'INSERT INTO DISPLAYED_IN VALUES({Id_no}, "{Name}");')
                mydb.commit()
            except: 
                print('Command could not be executed')
            break

        elif (userInput == '6'):
            break

        else: print('Not a valid input, please try again')

def updateOrDelete(mydb, mycursor, WhatToDo):
    print (f'Which table would you like to {WhatToDo.lower()} from?:\n1 - Art_Object\n2 - Artist\n3 - Exhibition\n4 - Collection\n5 - Painting\n6 - Sculpture/Statue\n7 - Other\n8 - Borrowed\n9 - Permanent collection\n10 - Displayed in\n11 - exit')
    choice = {'1':'ART_OBJECT','2':'ARTIST','3':'EXHIBITIONS','4':'COLLECTIONS','5':'PAINTING','6':'SCULPTURE_STATUE','7':'OTHER','8':'BORROWED','9':'PERMANENT_C','10':'DISPLAYED_IN'}
    attributes = {
    'ART_OBJECT':[['Id_no', 'integer'], ['Title', 'string'], ['Year', 'integer'], ['Description', 'string'], ['Epoch', 'string'], ['COO', 'string'], ['Artist', 'string']],
    'ARTIST':[['Name', 'string'], ['Description', 'string'], ['Main_style', 'string'], ['Date_died', 'integer'], ['Date_born', 'integer'], ['Epoch', 'string'], ['COO', 'string']],
    'EXHIBITIONS':[['Name', 'string'], ['Start_date', 'date'], ['End_date', 'date']],
    'COLLECTIONS':[['Name', 'string'], ['Address', 'string'], ['Type', 'string'], ['Contact_person', 'string'], ['Description', 'string'], ['Phone', 'string']],
    'PAINTING':[['Id_no', 'integer'], ['Drawn_on', 'string'], ['Paint_type', 'string'], ['Style', 'string']],
    'SCULPTURE_STATUE':[['Id_no', 'integer'], ['Weight', 'float'], ['Material', 'string'], ['Style', 'string'], ['Height', 'float']],
    'OTHER':[['Id_no', 'integer'], ['Style', 'string'], ['Type', 'string']],
    'BORROWED':[['Id_no', 'integer'], ['Date_borrowed', 'date'], ['Date_returned', 'date'], ['Collection_N', 'string']],
    'PERMANENT_C':[['Id_no', 'integer'], ['Date_acquired', 'date'], ['Cost', 'float'], ['Status', 'string']],
    'DISPLAYED_IN':[['Id_no','integer'],['Name','string']]
    }
    while(True):
        userInput = input('please input 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 or 11: ')
        if (userInput in ['1','2','3','4','5','6','7','8','9','10']):
            table = choice[userInput]
            break
        elif (userInput == '11'):
            return
        else: print('Not a valid input, please try again')

    if(WhatToDo == 'UPDATE'):
        toChange = [[],[]]
        for i in attributes[table]:
            while(True):
                print(f'Would you like to change the value of {i[0].lower()}?')
                userInput = input('please insert yes or no: ')
                if (userInput in ['y','Y','yes','Yes']):
                    newVal = inputChecker('What value would you like it to become?',i[1])
                    toChange[0].append(i)
                    toChange[1].append(newVal)
                    break
                if (userInput in ['n','N','no','No']):
                    break
                else: print('Not a valid input, please try again')

    print(f'What is the attribute for which the condition to {WhatToDo.lower()}?: ')
    attributeNum = 0
    for i in attributes[table]:
        attributeNum+=1
        print(f'{attributeNum} - {i[0]}')
    while(True):
        userChoice = input(f'please input and integer between 1 and {attributeNum}: ')
        if(userChoice.isdigit() == False or not(0 < int(userChoice) <= attributeNum)):
            print('Invalid input. Please try again')
        else: 
            userChoice = int(userChoice) -1
            break
    print('What is the condition on this attribute?')
    condition = inputChecker('Please input the condition of your choice',attributes[table][int(userChoice)][1])
    if(WhatToDo == 'DELETE'):
        command = f'{WhatToDo} FROM {table}'
    else: command = f'{WhatToDo} {table}'

    if(WhatToDo == 'UPDATE' and len(toChange[1])>0):
        if(toChange[0]):
            if (toChange[0][0][1] in ['string','date']):
                command += f' SET {toChange[0][0][0]} = "{toChange[1][0]}"'
            else: command += f' SET {toChange[0][0][0]} = {toChange[1][0]}'
        for i in range(len(toChange[0])):
            if(i != 0):
                if (toChange[0][i][1] in ['string','date']):
                    command += f', {toChange[0][i][0]} = "{toChange[1][i]}"'
                else: command += f', {toChange[0][i][0]} = {toChange[1][i]}'

    if (attributes[table][int(userChoice)][1] in ['string','date']):
        command += f' WHERE {attributes[table][int(userChoice)][0]} = "{condition}"'
    else: command += f' WHERE {attributes[table][int(userChoice)][0]} = {condition}'
    command+=';'
    if (len(toChange[1])>0):
        try:
            mycursor.execute(command)
            mydb.commit()
            print(f'{WhatToDo} was successful')
        except IOError as msg: 
            print('Command skipped: ', msg)
    else: print('Nothing to change. No command executed')

def addUsers(mydb, mycursor):
    while (True):
        print('Which User management action do you wish to do?: \n1 - Add User\n2 - edit User\n3 - Delete User\n4 - quit')
        userInput = input('please input 1, 2 or 3: ')

        if(userInput == '1'):
            username = input('What is the username of this user to add?: ')
            password = input('What is the password of this user to add?: ')
            try:
                mycursor.execute(f'CREATE USER {username}@localhost IDENTIFIED BY "{password}";')
                mycursor.execute(f'GRANT dataEntry@localhost TO {username}@localhost;')
                mycursor.execute(f'SET DEFAULT ROLE ALL TO {username}@localhost;')
                mydb.commit()
                print(f'{username} can now find, insert, update and delete data in the database')
            except:
                print('User already exists')
            break

        elif(userInput == '2'):
            username = input('What is the username of this user to edit?: ')
            newUsername = username
            print('Do you wish to change username or password to the user?: \n1 - Username\n2 - Password')
            userchoice = input('please input 1 or 2: ')
            if(userchoice == '1'):
                password = input('what is the current password')
                newUsername = input('what is the new username')

            elif(userchoice == '2'):
                password = input('what is the new password')

            try:
                mycursor.execute(f'DROP USER {username}@localhost;')
                mycursor.execute(f'CREATE USER {newUsername}@localhost IDENTIFIED BY "{password}";')
                mycursor.execute(f'GRANT dataEntry@localhost TO {newUsername}@localhost;')
                mycursor.execute(f'SET DEFAULT ROLE ALL TO {newUsername}@localhost;')
                mydb.commit()
                print(f'the change was successful')
            except:
                print('User does not exists')

            else: print('Not a valid input, please try again') 
            break

        elif(userInput == '3'):
            username = input('What is the username of this user to delete?: ')
            try:
                mycursor.execute(f'DROP USER {username}@localhost;')
                mydb.commit()
                print(f'{username} can not find, insert, update and delete data in the database anymore')
            except:
                print('User does not exists')
            break

        elif(userInput == '4'):
            break

        else: print('Not a valid input, please try again')   

def admin(mydb, mycursor):
    while(True):
        print('Do you wish to tye in a command or run a command(s) from a separate file?: \n1 - Type a command\n2 - Run a file\n3 - User management\n4 - quit')
        userInput = input('please input 1, 2, 3 or 4: ')
        if(userInput == '1'):
            command = input("Please type in your command that you wish to wish to execute on MYSQL: ")
            try:
                mycursor.execute(command)
                if (command.split(' ')[0] == 'SELECT'):
                    myresult = mycursor.fetchall()
                    for i in myresult:
                        print(i)
                else: mydb.commit()
            except: 
                print('Command could not be executed')
            print('\nDo you wish to do another action?')
            userQuit = input('type yes to do another action: ')
            if (userQuit not in ['y','Y','yes','Yes']): break

        elif(userInput == '2'):
            file = input('PLease input file location, or just file name if the incoming file is in the same folder')
            fd = open(file,'r')
            sqlFile = fd.read()
            fd.close()
            sqlCommands = sqlFile.split(';')

            for command in sqlCommands:
                try:
                    if command.strip() !='':
                        mycursor.execute(command)
                except IOError as msg:
                    print('Command skipped: ', msg)
            print('\nDo you wish to do another action?')
            userQuit = input('type yes to do another action: ')
            if (userQuit not in ['y','Y','yes','Yes']): break

        elif(userInput == '3'):
            addUsers(mydb, mycursor)
            print('\nDo you wish to do another action?')
            userQuit = input('type yes to do another action: ')
            if (userQuit not in ['y','Y','yes','Yes']): break

        elif(userInput == '4'):
            break

        else: print('Not a valid input, please try again')

def dataEntryUser(mydb, mycursor):
    while(True):
        while (True):
            print ('Do you wish to find data, input data, delete data, or update data?:\n1 - Select\n2 - Update\n3 - Delete\n4 - Input\n5 - exit')
            userInput = input('please input 1, 2, 3, 4, or 5: ')
            if (userInput == '1'):
                SearchSelection(mycursor)
                break

            elif (userInput == '2'):
                updateOrDelete(mydb, mycursor,'UPDATE')
                break

            elif (userInput == '3'):
                updateOrDelete(mydb, mycursor,'DELETE')
                break

            elif (userInput == '4'):
                insertData(mydb, mycursor)
                break
            
            elif(userInput == '5'):
                break

            else: print('Not a valid input, please try again')
        print('Do you wish to do another action?')
        userQuit = input('type yes to do another action: ')
        if (userQuit not in ['y','Y','yes','Yes']): break

def guest(mycursor):
    while(True):
        while (True):
            print ('Do you wish to find data?:\n1- Select\n2 - exit')
            userInput = input('please input 1 or 2')
            if (userInput == '1'):
                SearchSelection(mycursor)
            
            elif(userInput == '2'):
                break

            else: print('Not a valid input, please try again')
        print('Do you wish to do another action?')
        userQuit = input('type yes to do another action: ')
        if (userQuit not in ['y','Y','yes','Yes']): break

def main():
    print('Welcome to group __________\'s Museum Database')
    print('What is your role from the following:\n1 - Admin\n2 - Data entry user\n3 - Guest')
    while(True):
        userRole = input('please input 1, 2, or 3 to pick a role\n')
        if userRole in ['1','2']:
            username = input("What is your username?\n")
            passcode = input("What is your password?\n")
        elif (userRole == '3'):
            username = 'guest'
            passcode = None
        else: 
            print('invalid input. Please try again')
            continue
        try:
            mydb = mysql.connector.connect(
                host = '127.0.0.1',
                port = 3306,
                user = username,
                password = passcode)

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute('USE museum_database')
            break
        except:
            print('Invalid username or password, Please try again')

    if (userRole == '1'):
        admin(mydb, mycursor)

    if (userRole == '2'):
        dataEntryUser(mydb, mycursor)

    if (userRole == '3'):
        guest(mycursor)

if __name__ == "__main__":
    main()
 
