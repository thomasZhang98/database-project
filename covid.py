#!/usr/bin/python3
import pymysql
import getpass
databaseUsername = 'root'
databasePassword = 'root'
coviddb = 'covidtest'
userDataTable = 'user_data'
testSubjectType = 'test_subject'
centerEmployeeType = 'center_employee'
labEmployeeType = 'lab_employee'
testingSubjectInstructions = '''Please select from the following options:
a. Schedule an appointment
b. View tests
c. Delete a test
d. View personal information
e. Update personal information
'''

# Test status: 'PENDING' -> 'SENT TO LAB' -> 'POSITIVE/NEGATIVE'

if __name__ == '__main__':
    # Connect to covidtest database
    while True:
        try:
            connection = pymysql.connect(host='localhost', user=databaseUsername, password=databasePassword, database=coviddb, cursorclass=pymysql.cursors.DictCursor)
            print('covidtest database successfully connected!')
            break
        except pymysql.err.OperationalError as e:
            print('Error: %d: %s' % (e.args[0], e.args[1]))
            print('Please try again:')

    # Query if they want to sign up or log in.
    while True:
        loginOrSignup = input('Do you want to log in or sign up? a. "Log in" b. "Sign up": ')
        if loginOrSignup not in ['a', 'b']:
            print('Invalid value, please try again:')
        else:
            break

    # Retrieve username, password and role
    logged = False
    while True:
        if logged:
            break
        username = input('Please enter your username: ')
        password = getpass.getpass('Please enter your password: ')
        while True:
            role = input('Please choose your role from the following: a. "Testing Subject" b. "Testing Center Employee" c. "Lab Employee": ')
            if role in ['a', 'b', 'c']:
                break
            print('Invalid value, please try again:')

        if role == 'a':
            userType = testSubjectType
        elif role == 'b':
            userType = centerEmployeeType
        else:
            userType = labEmployeeType
        
        # If the operation is log in, get the 'user_id' from the 'user_data' table
        if loginOrSignup == 'a':
            # Check if the username is in the table
            try:
                cur = connection.cursor()
                # TODO: Use procedure/function to verify if a user_name exists instead
                stmt_select = 'SELECT user_name FROM user_data'
                cur.execute(stmt_select)
                rows = cur.fetchall()
                if {'user_name': username} not in rows:
                    print('Username not found, please try again.')
                else:
                    try:
                        # Log in the system by getting the 'user_id' if the 'user_name' is found.
                        cur2 = connection.cursor()
                        # TODO: Use procedure/function to login and get user_id instead
                        stmt_select2 = 'SELECT user_id FROM user_data WHERE user_name=\'' + username + '\' and password=\'' + password + '\' and user_type=\'' + userType + '\''
                        cur2.execute(stmt_select2)
                        uid = cur2.fetchone()['user_id']
                        print('uid: ' + str(uid))
                        break
                    except pymysql.err.OperationalError as e:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))
                        print('Please try again:')
                    cur2.close()
            except pymysql.err.OperationalError as e:
                print('Error: %d: %s' % (e.args[0], e.args[1]))
                print('Please try again:')
            cur.close()

        # Otherwise if the operation is signup, call the procedure to add a user in the 'user_data' table        
        else:
            # Check if the username is in the table
            try:
                cur = connection.cursor()
                # TODO: Use procedure/function to verify if a user_name exists instead
                stmt_select = 'SELECT user_name FROM user_data'
                cur.execute(stmt_select)
                rows = cur.fetchall()
                if {'user_name': username} in rows:
                    print('Username already taken, please choose another username.')
                else:
                    try:
                        # Add new records to the user_data table.
                        cur2 = connection.cursor()
                        # TODO: Use procedure/function to login and get user_id instead
                        
                        break
                    except pymysql.err.OperationalError as e:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))
                        print('Please try again:')
                    cur2.close()
            except pymysql.err.OperationalError as e:
                print('Error: %d: %s' % (e.args[0], e.args[1]))
                print('Please try again:')
            cur.close()

    # Testing Subject
    # CREATE: N/A
    # DELETE: They can delete schduled tests from the test table.
    # READ: They can read their personal information and look at their own tests and results.
    # UPDATE: They can update their personal information.
    if role == 'a':
        while True:
            option = input(testingSubjectInstructions)
            print(option)

    # Testing Center Employee
    # CREATE: They can create tests for testing subjects with initial status of 'PENDING'
    # DELETE: They can delete tests.
    # READ: They can read testing subjects' personal info and their tests in your testing center.
    # UPDATE: They can update tests status from 'PENDING' to 'SENT TO LAB'

    # Lab Employee
    # CREATE: N/A
    # DELETE: N/A
    # READ: They can read tests.
    # UPDATE: They can update tests status from 'SENT TO LAB' to 'POSITIVE/NEGATIVE'



    connection.close()

