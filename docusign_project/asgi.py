"""
ASGI config for docusign_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import dotenv
dotenv.load_dotenv() # Load environment variables from .env file


from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "docusign_project.settings")

application = get_asgi_application()
