# Bank Management System

## Description

This is a simple bank management system implemented in Python using singleton design-pattern. It allows you to create and close bank accounts, perform transactions such as deposits, withdrawals, and transfers, and view client information and transaction history. The system uses an SQLite database to store client data and transactions.

## Features

- **Create Account**: Add new clients with their personal details.
- **Close Account**: Remove client accounts from the system.
- **Show All Clients**: Display a list of all clients in the system.
- **Count Clients**: Get the total number of clients.
- **Client Actions**: Perform transactions such as withdrawals, deposits, and transfers for a specific client.
- **Check Balance**: View the current balance of a client.
- **Show Movements**: Display transaction history for a client.

## Installation

### Using Docker

1. **Build the Docker Image**:

    ```bash
    docker build -t bank-management-system .
    ```

2. **Run the Docker Container**:

    ```bash
    docker run -it --rm bank-management-system
    ```

   This command runs the application in an interactive terminal and removes the container when it exits.

### Without Docker

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project-directory>
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Follow the on-screen prompts to interact with the bank management system.

## Logging

The application logs debug information to `debug.log`. The log includes detailed information about actions performed and any errors encountered.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.


