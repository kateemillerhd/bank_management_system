# Bank Management System

A command-line bank management system built with Python and MySQL.

This project began as a basic banking application for creating accounts, checking account balance, and making deposits and withdrawals. It was expanded to use a relational MySQL database, support multiple accounts per customer, validate user input, and safely transfer funds between accounts.

## Features

- Create new customers and bank accounts
- Allow existing customers to open additional accounts
- Look up exiting customers by phone number
- View account and customer information
- Deposit funds
- Withdraw funds with insufficient balance protection
- Transfer funds between accounts
- Validate account IDs and monetary input
- Handle nonexistent accounts
- Prevent transfers between the same account
- Use database transactions to ensure transfers are completed atomically
- Store database credentials using environment variables

## Technologies

- Python
- MySQL
- MySQL Connector/Python
- python-dotenv
- Git

## Database Structure

The application uses two related tables.

### `customers`

| Column | Description |
| --- | --- |
| `customer_id` | Primary Key |
| `name` | Customer Name |
| `phone` | Unique customer phone number |

### `accounts`

| Column | Description |
| --- | --- |
| `account_id` | Primary Key |
| `customer_id` | Foreign Key referencing `customers.customer_id` |
| `balance` | Current account balance |

The relationship allows one customer to have multiple bank accounts.


```text
customers
--------------
customer_id (PK)
name
phone
    |
    | 1 : many
    v
accounts
--------------
account_id (PK)
customer_id (FK)
balance
```

## Banking Operations

### Create Account

When creating an account, the application searches for an existing customer using their phone number.

If the customer does not exist, a new customer record is created before the account is opened. If the customer already exists, the user can choose to open an additional account for that customer.

### View Account

Account information is retrieved using a SQL `JOIN` between the `accounts` and `customers` tables.

### Deposit and Withdraw

Deposits and withdrawals update the account balance in MySQL.

Withdrawals are rejected when:
 
- The account does not exist
- The amount is invalid
- The account has insufficient funds

### Transfer Funds

Funds can be transferred between two accounts.

Transfers use a database transaction so that both balance updates succeed or neither is committed. If a database error occurs during the transfer, the transaction is rolled back.

This prevents a situation where money is removed from the sender without being added to the receiver.  

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/kateemillerhd/bank_management_system.git
cd bank_management_system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install mysql-connector-python python-dotenv
```

### 4. Configure MySQL

Create a MySQL database:

```sql
CREATE DATABASE bank_management;
USE bank_management;
```

Create the customer table:

```sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
);
```

Create the account table:

```sql
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    customer_id INT NOT NULL,
    CONSTRAINT fk_accounts_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
```

### 5. Configure environment variables

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=bank_management
```

The `.env` file is excluded from Git so database credentials are not committed to the repository.

### 6. Run the application

```bash
python main.py
```

## Menu

The command-line interface provides the following operations:

```text
Bank Management System

1. Create Account
2. View Account
3. Deposit
4. Withdraw
5. Transfer
6.Exit
```