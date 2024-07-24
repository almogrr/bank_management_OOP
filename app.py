"""
Banking Application Module

This module provides functionality for managing a banking system, including account creation, 
deletion, and transactions such as deposits, withdrawals, and transfers.
"""

import logging
import sqlite3
from enum import Enum
from icecream import ic


# Configure logging
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BankActions(Enum):
    """
    Enum for various bank actions.
    """
    CREATE_ACCOUNT = 1
    CLOSE_ACCOUNT = 2
    SHOW_ALL_CLIENTS = 3
    COUNT_CLIENTS = 4
    CLIENT_ACTIONS = 5
    EXIT = 6

class ClientActions(Enum):
    """
    Enum for various client actions.
    """
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3
    CHECK_BALANCE = 4
    SHOW_MOVEMENTS = 5
    EXIT = 6

class Client:
    """
    Class representing a bank client.

    Attributes:
        id (int): Client ID.
        first_name (str): First name of the client.
        balance (float): Current balance of the client.
        occupation (str): Occupation of the client.
        movements (list): List of movements for the client.
    """
    def __init__(self, id, first_name, balance=0.0, occupation=None):
        self.id = id
        self.first_name = first_name
        self.balance = balance
        self.occupation = occupation
        self.movements = []

class Bank:
    """
    Class representing a bank.

    Manages client accounts and transactions.
    """
    def __init__(self):
        """
        Initializes the bank with a database connection and sets up the database schema.
        """
        self.db_connection = sqlite3.connect('bank.db')
        self.db_cursor = self.db_connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        """
        Creates the necessary tables in the database if they don't exist.
        """
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                balance REAL NOT NULL,
                occupation TEXT
            )
        ''')
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                amount REAL NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            )
        ''')
        self.db_connection.commit()

    def show_menu(self):
        """
        Displays the main menu and returns the user's choice.

        Returns:
            BankActions: The user's menu choice.
        """
        print("1. Create Account")
        print("2. Close Account")
        print("3. Show All Clients")
        print("4. Count Clients")
        print("5. Client Actions")
        print("6. Exit")
        choice = int(input("Select an option: "))
        return BankActions(choice)

    def show_client_menu(self):
        """
        Displays the client actions menu and returns the user's choice.

        Returns:
            ClientActions: The user's client action choice.
        """
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Transfer")
        print("4. Check Balance")
        print("5. Show Movements")
        print("6. Exit")
        choice = int(input("Select an action: "))
        return ClientActions(choice)

    def create_account(self, first_name, occupation=None):
        """
        Creates a new account with the given first name and optional occupation.

        Args:
            first_name (str): The first name of the client.
            occupation (str, optional): The occupation of the client.
        """
        self.db_cursor.execute("INSERT INTO clients (first_name, balance, occupation) VALUES (?, ?, ?)",
                               (first_name, 0.0, occupation))
        self.db_connection.commit()
        logging.info("Created account for %s with occupation %s.", first_name, occupation)
        ic(f"Created account for {first_name} with occupation {occupation}.")

    def close_account(self, client_id):
        """
        Closes an account with the given client ID.

        Args:
            client_id (int): The ID of the client whose account is to be closed.
        """
        self.db_cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        self.db_cursor.execute("DELETE FROM movements WHERE client_id=?", (client_id,))
        self.db_connection.commit()
        logging.info("Closed account with client ID %d.", client_id)
        ic(f"Closed account with client ID {client_id}.")

    def show_all_clients(self):
        """
        Displays all clients in the database.
        """
        self.db_cursor.execute("SELECT * FROM clients")
        clients = self.db_cursor.fetchall()
        logging.info("All clients: %s", clients)
        ic(f"All clients: {clients}")
        for client in clients:
            print(client)

    def count_clients(self):
        """
        Counts and displays the total number of clients.
        """
        self.db_cursor.execute("SELECT COUNT(*) FROM clients")
        count = self.db_cursor.fetchone()[0]
        logging.info("Total clients: %d", count)
        ic(f"Total clients: {count}")
        print(f"Total clients: {count}")

    def find_client(self, client_id):
        """
        Finds a client by ID.

        Args:
            client_id (int): The ID of the client to find.

        Returns:
            Client: The found client object, or None if not found.
        """
        self.db_cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        client_data = self.db_cursor.fetchone()
        if client_data:
            return Client(*client_data)
        return None

    def client_withdraw(self, client, amount):
        """
        Withdraws an amount from a client's account.

        Args:
            client (Client): The client from whom to withdraw the amount.
            amount (float): The amount to withdraw.
        """
        if amount <= client.balance:
            client.balance -= amount
            client.movements.append(f"Withdrawn: -{amount}")
            self.db_cursor.execute("UPDATE clients SET balance=? WHERE id=?", (client.balance, client.id))
            self.db_cursor.execute("INSERT INTO movements (client_id, action, amount) VALUES (?, ?, ?)",
                                   (client.id, 'Withdraw', -amount))
            self.db_connection.commit()
            logging.info("Withdrawn %.2f from client ID %d.", amount, client.id)
            ic(f"Withdrawn {amount} from client ID {client.id}.")
        else:
            logging.warning("Insufficient funds.")
            print("Insufficient funds.")

    def client_deposit(self, client, amount):
        """
        Deposits an amount into a client's account.

        Args:
            client (Client): The client into whom to deposit the amount.
            amount (float): The amount to deposit.
        """
        client.balance += amount
        client.movements.append(f"Deposited: +{amount}")
        self.db_cursor.execute("UPDATE clients SET balance=? WHERE id=?", (client.balance, client.id))
        self.db_cursor.execute("INSERT INTO movements (client_id, action, amount) VALUES (?, ?, ?)",
                               (client.id, 'Deposit', amount))
        self.db_connection.commit()
        logging.info("Deposited %.2f to client ID %d.", amount, client.id)
        ic(f"Deposited {amount} to client ID {client.id}.")

    def client_transfer(self, client_from, client_to_id, amount):
        """
        Transfers an amount from one client to another.

        Args:
            client_from (Client): The client from whom the amount is transferred.
            client_to_id (int): The ID of the client to whom the amount is transferred.
            amount (float): The amount to transfer.
        """
        client_to = self.find_client(client_to_id)
        if client_to:
            if amount <= client_from.balance:
                client_from.balance -= amount
                client_to.balance += amount
                client_from.movements.append(f"Transfer to {client_to_id}: -{amount}")
                client_to.movements.append(f"Transfer from {client_from.id}: +{amount}")
                self.db_cursor.execute("UPDATE clients SET balance=? WHERE id=?", (client_from.balance, client_from.id))
                self.db_cursor.execute("UPDATE clients SET balance=? WHERE id=?", (client_to.balance, client_to.id))
                self.db_cursor.execute("INSERT INTO movements (client_id, action, amount) VALUES (?, ?, ?)",
                                       (client_from.id, 'Transfer Out', -amount))
                self.db_cursor.execute("INSERT INTO movements (client_id, action, amount) VALUES (?, ?, ?)",
                                       (client_to.id, 'Transfer In', amount))
                self.db_connection.commit()
                logging.info("Transferred %.2f from client ID %d to client ID %d.", amount, client_from.id, client_to_id)
                ic(f"Transferred {amount} from client ID {client_from.id} to client ID {client_to_id}.")
            else:
                logging.warning("Insufficient funds.")
                print("Insufficient funds.")
        else:
            logging.warning("Client to transfer to (ID: %d) not found.", client_to_id)
            print("Client to transfer to not found.")

    def client_check_balance(self, client):
        """
        Checks and displays a client's balance.

        Args:
            client (Client): The client whose balance to check.
        """
        logging.info("Client ID %d balance: %.2f", client.id, client.balance)
        ic(f"Client ID {client.id} balance: {client.balance}")
        print(f"Client ID {client.id} balance: {client.balance}")

    def client_show_movements(self, client):
        """
        Shows all movements of a client's account.

        Args:
            client (Client): The client whose movements to show.
        """
        logging.info("Client ID %d movements: %s", client.id, client.movements)
        ic(f"Client ID {client.id} movements: {client.movements}")
        print(f"Client ID {client.id} movements:")
        for movement in client.movements:
            print(movement)

def main():
    """
    Main function to run the banking application.
    """
    bank = Bank()
    while True:
        action = bank.show_menu()
        if action == BankActions.CREATE_ACCOUNT:
            first_name = input("Enter first name: ")
            occupation = input("Enter occupation (optional): ")
            bank.create_account(first_name, occupation)
        elif action == BankActions.CLOSE_ACCOUNT:
            client_id = int(input("Enter client ID: "))
            bank.close_account(client_id)
        elif action == BankActions.SHOW_ALL_CLIENTS:
            bank.show_all_clients()
        elif action == BankActions.COUNT_CLIENTS:
            bank.count_clients()
        elif action == BankActions.CLIENT_ACTIONS:
            client_id = int(input("Enter client ID: "))
            client = bank.find_client(client_id)
            if client:
                while True:
                    client_action = bank.show_client_menu()
                    if client_action == ClientActions.WITHDRAW:
                        amount = float(input("Enter amount to withdraw: "))
                        bank.client_withdraw(client, amount)
                    elif client_action == ClientActions.DEPOSIT:
                        amount = float(input("Enter amount to deposit: "))
                        bank.client_deposit(client, amount)
                    elif client_action == ClientActions.TRANSFER:
                        transfer_id = int(input("Enter client ID to transfer to: "))
                        amount = float(input("Enter amount to transfer: "))
                        bank.client_transfer(client, transfer_id, amount)
                    elif client_action == ClientActions.CHECK_BALANCE:
                        bank.client_check_balance(client)
                    elif client_action == ClientActions.SHOW_MOVEMENTS:
                        bank.client_show_movements(client)
                    elif client_action == ClientActions.EXIT:
                        break
                    else:
                        print("Invalid action.")
            else:
                print("Client not found.")
        elif action == BankActions.EXIT:
            break
        else:
            print("Invalid action.")

if __name__ == "__main__":
    main()
