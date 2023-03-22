import psycopg2
import psycopg2.extras
import random



hostname = 'localhost'
database = 'banco'
username = 'postgres'
pwd = 'admin'
port_id = 5432
conn = None

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

          def acc_generator():  
               accvalue = ''
               for x in range(0,12):
                    accvalue+= f'{random.randint(0,9)}'
               select_script = 'SELECT * FROM accounts where acc = %s'
               listx = (f'{accvalue}',)
               cur.execute(select_script, listx)
               record = cur.fetchall()
               try:
                    record = record[2]

               except IndexError:
                    return accvalue
               else:
                    acc_generator()   

          def office_selector():
               x = random.randint(1,3)
               match x:
                    case 1:
                         return '102050'
                    case 2:
                         return '213921'
                    case 3:
                         return '777666'
          
          def acc_verify(accvalue):
               select_script = 'SELECT * FROM accounts WHERE acc = %s'
               select_record = (accvalue,)
               cur.execute(select_script, select_record) 
               record = cur.fetchall()
               try:
                    return record[0]
               except IndexError:
                    return '0'
               

          print('---------------------------------------------------------------------------------')
          print('|                                                                               |')
          print('|                                1 - login                                      |')
          print('|                               2 - sign in                                     |')
          print('|                                                                               |')
          print('---------------------------------------------------------------------------------')
          opt = int (input(''))

          match opt:
               case 1:
                    accvalue = input('type your account: ')
                    record = acc_verify(accvalue)
                    if record != '0':
                         pwdvalue = input('type your password: ')
                         if pwdvalue == record[-1]:
                              print('---------------------------------------------------------------------------------')
                              print('|                                                                               |')
                              print('|                              1 - withdraw                                     |')
                              print('|                               2 - deposit                                     |')
                              print('|                                                                               |')
                              print('---------------------------------------------------------------------------------')
                              opt = int (input(''))
                              match opt:
                                   case 1:
                                        withdraw = int(input('how much you wanna withdraw: '))
                                        balance = record[-2] + record[-3]
                                        if withdraw < balance:
                                             if withdraw > record[-2]:
                                                  newbalance = 0
                                                  newcredit = record[-3] - (withdraw - record[-2])
                                             else:
                                                  newbalance = record[-2] - withdraw
                                                  newcredit = record[-3]
                                             update_script = 'UPDATE accounts SET balance = %s, credit = %s WHERE acc = %s'
                                             listx = (newbalance, newcredit, f'{record[2]}')
                                             cur.execute(update_script,listx)
                                        else:
                                             print('you dont have this money')
                                   case 2:
                                        deposit = int(input('how much you wanna deposit: '))
                                        if record[-3] < 1000:
                                             newcredit = record[-3] + deposit
                                             if newcredit > 1000:
                                                  newbalance = newcredit - 1000
                                                  newcredit = 1000
                                        else:
                                             newbalance = record[-2] + deposit
                                             newcredit = 1000
                                        update_script = 'UPDATE accounts SET balance = %s, credit = %s WHERE acc = %s'
                                        listx = (newbalance, newcredit, f'{record[2]}')
                                        cur.execute(update_script,listx)
                                   case _:
                                        print('invalid option')
                         else:
                              print('invalid password')
                    else:
                         print('invalid account')
                    

               case 2:
                    namevalue = input('type your name: ')
                    docvalue = input('type your document: ')
                    pwdvalue = input('type your password: ')
                    accvalue = acc_generator()
                    print(accvalue)
                    officevalue = office_selector()
                    print(officevalue)
                    creditvalue = 1000
                    balancevalue = 0

                    print(f'your account number is {accvalue} and the office your office code is {officevalue}')                               


                    insert_script  = 'INSERT INTO accounts (doc, name, acc, office, credit, balance, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                    insert_values = [(docvalue, namevalue, accvalue, officevalue, creditvalue, balancevalue, pwdvalue)]
                    for record in insert_values:
                         cur.execute(insert_script, record)

               case _:
                    print ('invalid option')
          
          


except Exception as error:
     print(error)
finally:
     if conn is not None:
        conn.close()
