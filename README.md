# CashCompass

## Overview

CashCompass is an application designed to help users manage and share daily expenses among a group. It offers three methods for splitting expenses: exact amounts, percentages, or equal shares. Users can track their expenses, view balances, and generate downloadable balance sheets.

## Features

- **User Management**: Create, update, and manage user profiles.
- **Expense Tracking**: Add expenses and specify how they should be split.
- **Split Methods**: Divide expenses by exact amounts, percentages, or equal shares.
- **Balance Sheets**: Generate and download balance sheets in PDF or CSV formats.

## Tech Stack

- **Framework**: Django
- **Authentication**: JSON Web Tokens (JWT)
- **Database**: SQLite (default) or configure with other databases
- **Libraries**: Django REST Framework, PyJWT

## Setup and Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Foxtrot-14/CashCompass.git
    cd cashcompass
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser (Admin)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Authentication

The application uses JWT for authentication. Obtain a token by making a POST request to the `/register/` endpoint with your credentials.

- **Obtain Token**

    ```http
    POST /register/
    ```

    **Request Body:**

    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

    **Response:**

    ```json
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }
    ```

## API Endpoints

### User Management

- **Add User**

    ```http
    POST /api/users/
    ```

    **Request Body:**

    ```json
    {
        "username": "john_doe",
        "password": "securepassword",
        "email": "john@example.com"
    }
    ```

- **Update User**

    ```http
    PUT /api/users/{user_id}/
    ```

    **Request Body:**

    ```json
    {
        "username": "jane_doe",
        "email": "jane@example.com"
    }
    ```

- **Get User**

    ```http
    GET /api/users/{user_id}/
    ```

- **Delete User**

    ```http
    DELETE /api/users/{user_id}/
    ```

### Expense Management

- **Add Expense**

    ```http
    POST /api/expenses/
    ```

    **Request Body:**

    ```json
    {
        "amount": 100,
        "description": "Dinner",
        "split_method": "percentage",  # or "exact", "equal"
        "splits": [
            {"user_id": 1, "percentage": 50},
            {"user_id": 2, "percentage": 50}
        ]
    }
    ```

- **Get Expense**

    ```http
    GET /api/expenses/{expense_id}/
    ```

- **Delete Expense**

    ```http
    DELETE /api/expenses/{expense_id}/
    ```

### Balance Sheets

- **Generate Balance Sheet**

    ```http
    GET /api/balance-sheet/
    ```

    **Query Parameters:**

    - `format` (optional): `pdf` or `csv`

    Example:

    ```http
    GET /api/balance-sheet/?format=pdf
    ```

## Validation Rules

- **User Management**
    - `username`: Required, unique, non-empty string.
    - `password`: Required, minimum length of 8 characters.
    - `email`: Optional, valid email format.

- **Expense Management**
    - `amount`: Required, positive number.
    - `description`: Optional, maximum length of 255 characters.
    - `split_method`: Required, must be one of `"exact"`, `"percentage"`, or `"equal"`.
    - `splits`: Valid only if `split_method` is `"percentage"` or `"exact"`.

## Generating Balance Sheets

The balance sheet provides a summary of each user's net balance after all expenses have been accounted for. It can be downloaded as a PDF or CSV file from the `/api/balance-sheet/` endpoint.

## Contributing

We welcome contributions to the project! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your fork.
4. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using CashCompass! We hope it helps you manage and share your expenses efficiently.
