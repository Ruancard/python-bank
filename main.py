import psycopg2
import psycopg2.extras
import random

hostname = 'localhost'
database = 'bank'
username = 'postgres'
pwd = 'admin'
port_id = 5432
conn = None


def acc_generator():  
               acc = ''
               for x in range(0,12):
                    acc += f'{random.randint(0,9)}'
               select_script = f"SELECT * FROM accounts where acc = '{acc}'"
               cur.execute(select_script)
               record = cur.fetchall()
               try:
                    record = record[0]
               except IndexError:
                    return acc
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

class account:
    def __init__(self, doc, name, acc, office, credit, balance, pwd):
        self.doc = doc
        self.name = name
        self.acc = acc
        self.office = office
        self.credit = credit
        self.balance = balance
        self.pwd = pwd

def __main__():
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
                              cur.execute(f"SELECT * FROM accounts WHERE acc = '{accvalue}'") 
                              record = cur.fetchall()
                              try:
                                   record = record[0]
                              except:
                                   print("invalid account")
                                   __main__()
                              else:
                                   accessaccount = account(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                   print(f'hello {accessaccount.name}')
                                   pwdvalue = input('type your password: ')
                                   if pwdvalue == accessaccount.pwd:
                                        print('---------------------------------------------------------------------------------')
                                        print('|                                                                               |')
                                        print('|                              1 - withdraw                                     |')
                                        print('|                               2 - deposit                                     |')
                                        print('|                                                                               |')
                                        print('---------------------------------------------------------------------------------')
                                        opt = int (input(''))
                                        match opt:
                                             case 1:
                                                  value = int(input('type withdraw value: '))

                                                  if value <= (accessaccount.balance):
                                                       update_script = f"UPDATE accounts SET balance = {accessaccount.balance - value} WHERE acc = '{accessaccount.acc}'"

                                                  elif value <= (accessaccount.balance + accessaccount.credit):
                                                       credit = accessaccount.balance - value
                                                       update_script = f"UPDATE accounts SET balance = 0, credit = {accessaccount.credit + credit} WHERE acc = '{accessaccount.acc}'"

                                                  else:
                                                       print("you don't have this limit")
                                                       __main__()

                                                  cur.execute(update_script)
                                                  cur.execute(f"SELECT * FROM accounts WHERE acc = '{accvalue}'") 
                                                  record = cur.fetchall()
                                                  record = record[0]
                                                  accessaccount = account(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                                  print(f"withdraw success and now your balance is {accessaccount.balance} and your credit is {accessaccount.credit}")

                                             case 2:

                                                  value = int(input('type deposit value: '))
                                                  if accessaccount.credit < 1000:
                                                       credit = accessaccount.credit + value
                                                       if credit > 1000:
                                                            balance = credit - 1000
                                                            credit = 1000
                                                            update_script = f"UPDATE accounts SET balance = {balance}, credit = {credit} WHERE acc = '{accessaccount.acc}'"
                                                       else:
                                                            update_script = f"UPDATE accounts SET credit = {credit} WHERE acc = '{accessaccount.acc}'"
                                                  else:
                                                       balance = accessaccount.balance + value
                                                       update_script = f"UPDATE accounts SET balance = {balance} WHERE acc = '{accessaccount.acc}'"
                                                  cur.execute(update_script)
                                                  cur.execute(f"SELECT * FROM accounts WHERE acc = '{accvalue}'") 
                                                  record = cur.fetchall()
                                                  record = record[0]
                                                  accessaccount = account(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                                                  print(f"deposit success and now your balance is {accessaccount.balance} and your credit is {accessaccount.credit}")    
                    
                                             case _:
                                                    print('invalid number')
                                                    __main__()

                         case 2:
                              name = input('type your name: ')
                              doc = input('type your document: ')
                              pwd = input('type your password: ')
                              acc = acc_generator()
                              print(acc)
                              office = office_selector()
                              print(office)
                              credit = 1000
                              balance = 0
                              print(f'your account number is {acc} and the office your office code is {office}')

                              insert_script  = f"INSERT INTO accounts (doc, name, acc, office, credit, balance, password) VALUES ('{doc}', '{name}', '{acc}', '{office}', {credit}, {balance}, '{pwd}')"
                              cur.execute(insert_script)
                         case _:
                              print('invalid number')
                              __main__()

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
              
              __main__() 
               
except Exception as error:
     print(error)
finally:
     if conn is not None:
        conn.close()
