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
    cd CashCompass
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python3 -m virtualenv venv
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

## API Endpoints
The application uses JWT for authentication. Obtain a token by making a POST request to the `account/register/` endpoint with your credentials.

- **Register Usre**

    ```http
    POST /account/register/
    ```

    **Request Body:**

    ```json
    {
    "email":"jhondoe3@gmail.com",
    "phone":"456121",
    "name":"Jhon Doe",
    "password1":"test",
    "password2":"test"
    }
    ```

    **Response:**

    ```json
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }
    ```

**Login**

    ```http
    POST /account/login/
    ```

 **Request Body:**

    ```json
    {
    "identifier":"jhondoe3@gmail.com",
    "password1":"test"
    }
    ```

 **Response:**

    ```json
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }
    ```

### Expense Management

- **Add Expense**

    ```http
    POST /api/expense-create/
    ```

 **Request Body:**

    ```json
    {
    "title": "Office Supplies",
        "description": "Purchase of office supplies including pens and paper.",
        "type": 2,
        "cost": 200,
        "participants":[{
        "participant":3,
        "contribution":25
        },{
        "participant":4,
        "contribution":50
        }]
    }
    ```
- **Get All Expenses for a User**

    ```http
    GET /api/expense/
    Authorization: Bearer YOUR_AUTHORIZATION_TOKEN
    ```

- **Get Expense**

    ```http
    GET /api/expense/{expense_id}/
    ```

- **Edit Expense**

    ```http
    POST /api/expense/{expense_id}/
    ```

 **Request Body:**

    ```json
    {
    "title": "Office Supplies",
        "description": "Purchase of office supplies including pens and paper.",
        "type": 3, //changin type
        "cost": 200,
        "participants":[{
        "participant":3,
        "contribution":25
        },{
        "participant":4,
        "contribution":50
        }]
    }
    ```

- **Delete Expense**

    ```http
    DELETE /api/expense/{expense_id}/
    ```

### Balance Sheets

- **Generate Balance Sheet**

    ```http
    GET /balance-sheet/{balance_id}/
    ```

## Validation Rules

- **User Management**
    - `email`: Required, unique, non-empty string.
    - `phone`: Required, valid phone number.
    - `name`: Required, valid name.
    - `password`: Required.

- **Expense Management**
    - `title`: Required, string.
    - `description`: Optional, maximum length of 255 characters.
    - `type`: Required, an integer 1 for `"exact"`, 2 for `"equal"`, or 3 for `"percentage"`.
    - `participants`: Required, an array of objects, every object must have `participant` and if type is `"exact"` or `"percentage"` then the object must also contain `contribution`.

## Generating Balance Sheets

The balance sheet provides a summary of each user's net balance after all expenses have been accounted for. It can be downloaded as CSV file from the `/api/balance-sheet/` endpoint.

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
