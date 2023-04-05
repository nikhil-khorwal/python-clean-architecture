# python-ecommerce-clean-architecture
Ecommerce API built with Flask followed by clean architecture

#### Features

- ##### Admin Users Can
  - Manage Category (Add, Update, View and Delete).
  - Manage Products (Add, Update, View and Delete).
  - Manage Users (Add, Update, View and Delete).
  - Manage Orders (View and Process).
   
    
- ##### Users Can
  - Signup
  - Login
  - Update Profile.
  - Add to Cart.
  - While Checkout, User should give the address to deliver.
  - Manage delivery address

## Approach
- Used clean architecture for implementing Ecommerce API.

## Naming Conventions
- Folder Name : your_folder_name
- File Name : your_file_name.py
- Class Name : YourClassName
- Variable Name : yourVariableName
- Function Name :your_function_name

## How to run a project
Use below command to run project based on your requirement
- Clone project from git.
- Run command ```docker-compose up```
- For creating environment: ```python -m venv myenv```
- After that run this command ```pip install -r requirements.txt```
- After that run this command ```cd app```
- For development debug: ```flask run``` for starting the server
- For run the testcases: ```pytest -svv```

## Directory Structure
```s
├── app
│   ├── application
│   │   ├── rest
│   │   │   ├── address.py
│   │   │   ├── cart.py
│   │   │   ├── category.py
│   │   │   ├── order.py
│   │   │   ├── product.py
│   │   │   └── user.py
│   │   ├── app.py
│   │   └── config.py
│   ├── core
│   │   ├── db
│   │   │   └── postgres_configuration.py
│   │   ├── error
│   │   │   ├── request.py
│   │   │   └── response.py
│   │   ├── methods
│   │   │   └── core_method.py
│   │   └── middleware
│   │       └── user_middleware.py
│   ├── ecommerce
│   │   └── feature1
│   │       ├── domain
│   │       ├── repository
│   │       ├── requests
│   │       ├── serializers
│   │       └── use_cases
│   ├── test
│   │   ├── ecommerce
│   │   │    ├── feature1
│   │   │    │    ├── domain
│   │   │    │    │   └── __init__.py
│   │   │    │    ├── repository
│   │   │    │    │   └── __init__.py
│   │   │    │    ├── requests
│   │   │    │    │   └── __init__.py
│   │   │    │    ├── serializers
│   │   │    │    │   └── __init__.py
│   │   │    │    ├── use_cases
│   │   │    │    │   └── __init__.py
│   │   │    │    └── __init__.py
│   │   │    └── __init__.py
│   │   └── __init__.py
│   ├── .flake8
│   ├── pytest.ini
│   └── wsgi.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```