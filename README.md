# DocuSign Django Integration Project

This project is a Django-based web application that integrates with the [DocuSign eSignature API](https://developers.docusign.com/docs/esign-rest-api/). It provides a backend for sending, managing, and tracking electronic signatures using DocuSign, with a RESTful API built using Django REST Framework.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- Django 4.2.x backend
- RESTful API with Django REST Framework
- DocuSign eSignature API integration
- Environment-based configuration
- Secure management of secrets using `.env` files

---

## Requirements

- Python 3.8+
- pip (Python package manager)
- [DocuSign Developer Account](https://developers.docusign.com/)
- (Recommended) [virtualenv](https://virtualenv.pypa.io/) for isolated Python environments

---

## Installation

1. **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd docusign_project
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv ../myenv
    source ../myenv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## Configuration

1. **Create a `.env` file** in the project root (same directory as `manage.py`):

    ```env
    # DocuSign API credentials
    DOCUSIGN_INTEGRATOR_KEY=your_integrator_key
    DOCUSIGN_USER_ID=your_user_id
    DOCUSIGN_PRIVATE_KEY_PATH=path/to/private.key
    DOCUSIGN_BASE_URL=https://demo.docusign.net/restapi

    # Django settings
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    ```

2. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

3. **Create a superuser (optional, for admin access):**
    ```sh
    python manage.py createsuperuser
    ```

---

## Usage

- **Run the development server:**
    ```sh
    python manage.py runserver
    ```

- **API Endpoints:**  
  The API endpoints will be available at `http://localhost:8000/` (or as configured).

- **Admin Panel:**  
  Visit `http://localhost:8000/admin/` to access the Django admin interface.

---

## Project Structure

```
docusign_project/
├── manage.py
├── docusign_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── <your_app>/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── ...
├── requirements.txt
├── .env
└── .gitignore
```

---

## Development

- **Code Formatting:**  
  Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) guidelines.
- **Environment Variables:**  
  Never commit your `.env` file or secrets to version control.
- **Adding Dependencies:**  
  Use `pip install <package>` and then `pip freeze > requirements.txt`.

---

## Testing

- **Run tests:**
    ```sh
    python manage.py test
    ```
- **Test coverage:**  
  You can use `coverage` or `pytest` for advanced testing and coverage reports.

---

## Troubleshooting

- **Dependency Issues:**  
  Ensure your Python version matches the requirements. If you get version errors, check [PyPI](https://pypi.org/) for the latest compatible versions.
- **DocuSign API Issues:**  
  Make sure your credentials are correct and you are using the sandbox environment for testing.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Credits

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [DocuSign eSignature API](https://developers.docusign.com/docs/esign-rest-api/)
