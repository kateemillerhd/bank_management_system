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

def create_account(customer_id, initial_balance):
    if initial_balance < 0:
        print('Initial balance cannot be less than $0.00')
        return
    
    cursor = connection.cursor()    
    
    sql = """
        INSERT INTO accounts (customer_id, balance)
        VALUES (%s, %s)
    """
    values = (customer_id, initial_balance)

    cursor.execute(sql, values)
    connection.commit()

    account_id = cursor.lastrowid

    cursor.close()

    print(f'Account {account_id} created successfully.')

def get_account(account_id):
    cursor = connection.cursor()
    
    sql = """
        SELECT accounts.account_id, customers.name, customers.phone, accounts.balance
        FROM accounts 
        JOIN customers
            ON accounts.customer_id = customers.customer_id 
        WHERE accounts.account_id = %s
    """

    value = (account_id,)

    cursor.execute(sql, value)
    account = cursor.fetchone()

    if account is None:
        print('Account not found.')
        cursor.close()
        return
    
    account_no = account[0]
    cust_name = account[1]
    cust_phone = account[2]
    balance = account[3]

    print(f'\nAccount Number: {account_no}'
          f'\nName: {cust_name}'
          f'\nPhone: {cust_phone}'
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
    
    sql = "SELECT balance FROM accounts WHERE account_id = %s"
    value = (account_id,)

    cursor.execute(sql, value)
    account = cursor.fetchone()

    if account is None:
        print('Account not found.')
        cursor.close()
        return

    if account[0] >= amount:
        sql = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_id = %s
        """
        values = (amount, account_id)
        
        cursor.execute(sql, values)
        connection.commit()

        print('\nWithdrawal successful.')
    else:
        print('\nInsufficient balance.')

    cursor.close()

def validate_id():
    while True:
        account_id = input('Account ID Number: ')
        if account_id.isdigit():
            return int(account_id)
        print('Invalid Account ID Number.')

def get_valid_amount(prompt, allow_zero=False):
    while True:
        amount = input(prompt)

        try:
            amount = float(amount)
            if amount < 0 or (amount == 0 and not allow_zero):
                print('Amount must be positive.')
                continue
            return amount
        except ValueError:
            print('Amount must be a valid dollar amount.')            

def get_customer_by_phone(phone):
    cursor = connection.cursor()

    sql = "SELECT * FROM customers WHERE phone = %s"
    value = (phone,)

    cursor.execute(sql, value)
    customer = cursor.fetchone()

    cursor.close()

    return customer

def create_customer(name, phone):
    cursor = connection.cursor()

    sql = "INSERT INTO customers (name, phone) VALUES (%s, %s)"
    values = (name, phone)

    cursor.execute(sql, values)
    connection.commit()

    customer_id = cursor.lastrowid

    cursor.close()

    return customer_id

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
        phone = input("Phone: ")

        initial_balance = get_valid_amount(
            'Inital balance: ',
            allow_zero=True
        )

        customer = get_customer_by_phone(phone)

        if customer is None:
            customer_id = create_customer(name, phone)
        else: 
            customer_id = customer[0]

        create_account(customer_id, initial_balance)

    # VIEW ACCOUNT/GET BALANCE
    elif choice == "2":
        account_id = validate_id()
        get_account(account_id)

    # DEPOSIT
    elif choice == "3":
        account_id = validate_id()
        amount = get_valid_amount('Amount to deposit: ')                
        deposit(account_id, amount)

    # WITHDRAWAL    
    elif choice == "4":
        account_id = validate_id()
        amount = get_valid_amount('Amount to withdraw: ')
        withdraw(account_id, amount)

    # EXIT
    elif choice == "5":
        break

    else:
        print('Please choose an option from 1-5.')

connection.close()