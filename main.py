import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

def create_account(name, initial_balance):
    if initial_balance < 0:
        print('Initial balance cannot be less than $0.00')
        return
    
    cursor = connection.cursor()    
    
    sql = "INSERT INTO accounts (name, balance) VALUES (%s, %s)"
    values = (name, initial_balance)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()

    print('Account created successfully.')

def get_account(account_id):
    cursor = connection.cursor()
    
    sql = "SELECT * FROM accounts WHERE account_id = %s"
    value = (account_id,)

    cursor.execute(sql, value)
    account = cursor.fetchone()

    if account is None:
        print('Account not found.')
        cursor.close()
        return
    
    account_no = account[0]
    cust_name = account[1]
    balance = account[2]

    print(f'\nAccount Number: {account_no}'
          f'\nName: {cust_name}'
          f'\nBalance: ${balance}'
    )

    cursor.close()

def deposit(account_id, amount):
    if amount <= 0:
        print('Deposit amount must be positive.')
        return
    
    cursor = connection.cursor()
    
    sql = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_id = %s
    """
    values = (amount, account_id)

    cursor.execute(sql, values)
    
    if cursor.rowcount == 0:
        print('Account not found.')
        cursor.close()
        return
    
    connection.commit()
    cursor.close()

    print('Deposit successful.')

def withdraw(account_id, amount):
    if amount <= 0:
        print('Withdrawal amount must be positive.')
        return

    cursor = connection.cursor()
    
    sql = "SELECT * FROM accounts WHERE account_id = %s"
    value = (account_id,)

    cursor.execute(sql, value)
    account = cursor.fetchone()

    if account is None:
        print('Account not found.')
        cursor.close()
        return

    if account[2] >= amount:
        sql = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_id = %s
        """
        values = (amount, account_id)
        
        cursor.execute(sql, values)
        connection.commit()

        print('\nWithdrawal succesful.')
    else:
        print('\nInsufficient balance.')

    cursor.close()

# create_account("Test Customer", 500.00)
# get_account(1)
# deposit(1, 100)
# withdraw(100, 200.00)

while True:
    print("\nBank Management System")
    print("1. Create Account")
    print("2. View Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Exit")

    choice = input("\nChoose an option: ")

    # CREATE ACCOUNT
    if choice == "1":
        name = input("Name: ")
        
        while True:
            initial_balance = input("Initial balance: ")
            
            try:
                initial_balance = float(initial_balance)

                if initial_balance < 0:
                    print('Initial balance cannot be less than $0.00')
                    continue

                break

            except ValueError:
                print('Initial balance must be valid dollar amount, or $0')
            

        create_account(name, initial_balance)

    # VIEW ACCOUNT/GET BALANCE
    elif choice == "2":
        
        while True:
            account_id = input("Account ID Number: ")
        
            if account_id.isdigit():
                account_id = int(account_id)
                break

            print('Invalid Acount ID Number.')
        
        get_account(account_id)

    # DEPOSIT
    elif choice == "3":
        while True:
            account_id = input("Account ID Number: ")

            if account_id.isdigit():
                account_id = int(account_id)
                break

            print('Invalid Account ID Number.')

        while True:
            amount = input("Amount to deposit: ")
            
            try:
                amount = float(amount)
                break
            except ValueError:
                print('Amount must be a valid dollar amount.')
                

        deposit(account_id, amount)

    # WITHDRAWAL    
    elif choice == "4":
        
        while True:
            account_id = input("Account ID Number: ")
            
            if account_id.isdigit():
                account_id = int(account_id)
                break
            
            print('Invalid Account ID Number.')

        while True:

            amount = input("Amount to withdraw: ") 
    
            try: 
                amount = float(amount)
                break
            except ValueError:
                print('Amount must be valid dollar amount.')

        withdraw(account_id, amount)

    # EXIT
    elif choice == "5":
        break

    else:
        print('Please choose an option from 1-5.')

connection.close()