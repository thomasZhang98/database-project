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
loggedInId = -1
userType = None
subType = None

testingSubjectInstructions = '''Please select from the following options:
a. Schedule an appointment
b. View tests
c. Unschedule a scheduled test
d. View personal information
e. Update personal information
f. exit
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
        if loginOrSignup in ['a', 'b']:
            break
        print('Invalid value, please try again:')

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
                stmt_check_if_username_exists = 'CALL check_if_username_exists(' + username + ')'
                cur.execute(stmt_check_if_username_exists)
                found = cur.fetchone()
                if found:
                    try:
                        # Log in the system by getting the 'user_id' if the 'user_name' is found.
                        cur2 = connection.cursor()
                        stmt_getUserId = 'CALL getUserId(\'' + username + '\', \'' + password + '\', \'' + userType + '\')'
                        cur2.execute(stmt_getUserId)
                        loggedInId = cur2.fetchone()['user_id']
                        print(username + ' logged in')
                    except pymysql.err.OperationalError as e:
                        print('Error: %d: %s' % (e.args[0], e.args[1]))
                        print('Please try again:')
                    cur2.close()
                else:
                    'Username not found, please try again:'
            except pymysql.err.OperationalError as e:
                print('Error: %d: %s' % (e.args[0], e.args[1]))
                print('Please try again:')
            cur.close()

        # Otherwise if the operation is signup, call the procedure to add a user in the 'user_data' table        
        else:
            try:
                cur = connection.cursor()
                stmt_check_if_username_exists = 'CALL check_if_username_exists(' + username + ')'
                cur.execute(stmt_check_if_username_exists)
                found = cur.fetchone()
                # Sign up a test subject
                if userType == testSubjectType:
                    while True:
                        subtype = input('What kind of testing subject is this? a. Student b. Professor c. Staff')
                        if subtype in ['a', 'b', 'c']:
                            break
                        print('Invalid value, please try again:')
                    
                    full_name = input('What is the full name?')
                    birthdate = input('What is the birthdate?')
                    gender = input('What is the gender?')
                    phone_number = input('What is the 10-digit phone number?')
                    email = input('What is the email?')
                    address = input('What is the address?')
                    test_frequency = input('What is the test frequency?')
                    if subtype == 'a':
                        try:
                            college = input('What is the college?')
                            major = input('What is the major?')
                            year_graduate = int(input('What is the year of graduation?'))
                            # Add new records to the student table.
                            cur2 = connection.cursor()
                            stmt_insert_student = 'CALL insert_student(\'' + full_name + '\', \''
                            + birthdate + '\', \'' 
                            + gender + '\', \'' 
                            + phone_number + '\', \'' 
                            + email + '\', \''
                            + address + '\', \'' 
                            + test_frequency + '\', \'' 
                            + college + '\', \'' 
                            + major + '\', \'' 
                            + year_graduate + '\', \'' + '\')'
                            cur2.execute(stmt_insert_student)
                            loggedInId = cur2.fetchone()['user_id']
                            break
                        except pymysql.err.OperationalError as e:
                            print('Error: %d: %s' % (e.args[0], e.args[1]))
                            print('Please try again:')
                    elif subtype == 'b':
                        try:
                            college = input('What is the college?')
                            department = input('What is the department?')
                            # Add new records to the professor table.
                            cur2 = connection.cursor()
                            stmt_insert_professor = 'CALL insert_professor(\'' + full_name + '\', \'' 
                            + birthdate + '\', \'' 
                            + gender + '\', \'' 
                            + phone_number + '\', \'' 
                            + email + '\', \''
                            + address + '\', \''
                            + test_frequency + '\', \''
                            + college + '\', \''
                            + department + '\')'
                            cur2.execute(stmt_insert_professor)
                            loggedInId = cur2.fetchone()['user_id']
                            break
                        except pymysql.err.OperationalError as e:
                            print('Error: %d: %s' % (e.args[0], e.args[1]))
                            print('Please try again:')
                    else:
                        try:
                            department = input('What is the department?')
                            job_title = input('What is the job title?')
                            # Add new records to the staff table.
                            cur2 = connection.cursor()
                            stmt_insert_staff = 'CALL insert_staff(\'' + full_name + '\', \'' 
                            + birthdate + '\', \'' 
                            + gender + '\', \'' 
                            + phone_number + '\', \'' 
                            + email + '\', \''
                            + address + '\', \''
                            + test_frequency + '\', \''
                            + department + '\', \''
                            + job_title + '\')'
                            cur2.execute(stmt_insert_staff)
                            loggedInId = cur2.fetchone()['user_id']
                            break
                        except pymysql.err.OperationalError as e:
                            print('Error: %d: %s' % (e.args[0], e.args[1]))
                            print('Please try again:')

                # Sign up a testing center employee
                elif userType == centerEmployeeType:
                    while True:
                        full_name = input('What is the full name?')
                        start_date = input('What is the start date? Use format of yyyy-mm-dd')
                        center_id = input('What is the center id?')
                        phone_number = int(input('What is the phone number?'))
                        email = input('What is the email?')
                        try:
                            # Add new records to the center_employee table.
                            cur2 = connection.cursor()
                            stmt_insert_center_employee = 'CALL insert_center_employee(\'' + full_name + '\', \'' 
                            + start_date + '\', \'' 
                            + center_id + '\', \''
                            + phone_number + '\', \'' 
                            + email + '\')'
                            cur2.execute(stmt_insert_center_employee)
                            loggedInId = cur2.fetchone()['user_id']
                            break
                        except pymysql.err.OperationalError as e:
                            print('Error: %d: %s' % (e.args[0], e.args[1]))
                            print('Please try again:')
                        cur2.close()

                # Sign up a lab employee type
                elif userType == labEmployeeType:
                    while True:
                        full_name = input('What is the full name?')
                        start_date = input('What is the start date? Use format of yyyy-mm-dd')
                        phone_number = int(input('What is the phone number?'))
                        email = input('What is the email?')
                        try:
                            # Add new records to the lab_employee table.
                            cur2 = connection.cursor()
                            stmt_insert_lab_employee = 'CALL insert_lab_employee(\'' + full_name + '\', \'' + start_date + '\', \'' + phone_number + '\', \'' + email + '\')'
                            cur2.execute(stmt_insert_lab_employee)
                            loggedInId = cur2.fetchone()['user_id']
                            break
                        except pymysql.err.OperationalError as e:
                            print('Error: %d: %s' % (e.args[0], e.args[1]))
                            print('Please try again:')
                        cur2.close()
                
                print('Account succesfully signed up and logged in!')
                break
            except pymysql.err.OperationalError as e:
                print('Error: %d: %s' % (e.args[0], e.args[1]))
                print('Please try again:')
            cur.close()

    # Testing Subject
    # CREATE: N/A
    # DELETE: N/A
    # READ: They can read their personal information and look at their own tests and results.
    # UPDATE: They can update their personal information. Update test status from 'scheduled' to 'cancelled'
    if role == 'a':
        while True:
            while True:
                option = input(testingSubjectInstructions)
                if option in ['a', 'b', 'c', 'd', 'e', 'f']:
                    break
                print('Invalid value, please try again:')

            # Schedule an appointment
            if option == 'a':
                test_date = input('Which date do you want to get tested? Answer in the format of yyyy-mm-dd')
                try:
                    # Add a new test to the table
                    cur2 = connection.cursor()
                    stmt_add_test = 'CALL add_test(\'' + user_id + '\', \'' + test_date + '\')'
                    cur2.execute(stmt_add_test)
                    print('Test successfully scheduled!')
                except pymysql.err.OperationalError as e:
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                    print('Please try again:')
                cur2.close()


            # View tests
            elif option == 'b':
                try:
                    # Retrieve tests for the logged in account
                    cur2 = connection.cursor()
                    stmt_get_tests_for_user = 'CALL get_tests(\'' + loggedInId + '\')'
                    cur2.execute(stmt_get_tests_for_user)
                    tests = cur2.fetchall()
                    for test in tests:
                        print(test)
                except pymysql.err.OperationalError as e:
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                    print('Please try again:')
                cur2.close()

            # Unschedule a scheduled test
            elif option == 'c':
                test_id_to_be_unscheduled = input('Which test id do you want to unschedule?')
                try:
                    # Unschedule scheduled tests for the logged in account
                    cur2 = connection.cursor()
                    stmt_unschdule_test = 'CALL unschedule_test(\'' + test_id_to_be_unscheduled + '\')'
                    cur2.execute(stmt_unschdule_test)
                    print('Test successfully unscheduled')
                except pymysql.err.OperationalError as e:
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                    print('Please try again:')
                cur2.close()

            # View personal information
            elif option == 'd':
                try:
                    # Retrieve the account info for the current logged in account
                    cur2 = connection.cursor()
                    stmt_get_account_info = 'CALL get_account_info(\'' + loggedInId + '\')'
                    cur2.execute(stmt_get_account_info)
                    account_info = cur2.fetchall()
                    for info in account_info:
                        print(info)
                except pymysql.err.OperationalError as e:
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                    print('Please try again:')
                cur2.close()

            # Update personal information
            elif option == 'e':
                field = input('Which field do you want to modify?')
                newValue = input('What value do you want to ')
                try:
                    # Update the field of the logged in account to the new value
                    cur2 = connection.cursor()
                    stmt_update_account_info = 'CALL update_account_info(\'' + loggedInId + '\', \'' + field + '\', \'' + newValue + '\')'
                    cur2.execute(stmt_update_account_info)
                    print('Field ' + field + 'updated!')
                except pymysql.err.OperationalError as e:
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                    print('Please try again:')
                cur2.close()

            # Exit the program
            elif option == 'f':
                print('Logged out!')
                break

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

