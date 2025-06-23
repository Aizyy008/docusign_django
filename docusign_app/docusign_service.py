import base64
import os
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, RecipientViewRequest
from docusign_esign.models import RecipientIdentityVerification, RecipientPhoneAuthentication
from docusign_esign.client.api_exception import ApiException
import jwt
import time
import requests
import json
import uuid

# DocuSign Configuration
DOCUSIGN_INTEGRATION_KEY = os.getenv("DOCUSIGN_INTEGRATION_KEY")
DOCUSIGN_USER_ID = os.getenv("DOCUSIGN_USER_ID")
DOCUSIGN_ACCOUNT_ID = os.getenv("DOCUSIGN_ACCOUNT_ID")
DOCUSIGN_BASE_PATH = os.getenv("DOCUSIGN_BASE_PATH", "https://demo.docusign.net/restapi")
DOCUSIGN_IDV_WORKFLOW_ID = os.getenv("DOCUSIGN_IDV_WORKFLOW_ID")
DOCUSIGN_PRIVATE_KEY = os.getenv("DOCUSIGN_PRIVATE_KEY")

# Debug prints for environment variables
print("\n=== DocuSign Environment Variables ===")
print("Integration Key:", DOCUSIGN_INTEGRATION_KEY)
print("User ID:", DOCUSIGN_USER_ID)
print("Account ID:", DOCUSIGN_ACCOUNT_ID)
print("Base Path:", DOCUSIGN_BASE_PATH)
print("Workflow ID:", repr(DOCUSIGN_IDV_WORKFLOW_ID))
print("Private Key Length:", len(DOCUSIGN_PRIVATE_KEY) if DOCUSIGN_PRIVATE_KEY else 0)
print("=====================================\n")

# Validate required environment variables
if not all([DOCUSIGN_INTEGRATION_KEY, DOCUSIGN_USER_ID, DOCUSIGN_ACCOUNT_ID, DOCUSIGN_IDV_WORKFLOW_ID, DOCUSIGN_PRIVATE_KEY]):
    raise ValueError("Missing required DocuSign environment variables")

# Validate workflow ID format
try:
    # Remove any whitespace and quotes
    workflow_id = DOCUSIGN_IDV_WORKFLOW_ID.strip().strip('"\'')
    # Try to parse as UUID to validate format
    uuid.UUID(workflow_id)
    DOCUSIGN_IDV_WORKFLOW_ID = workflow_id
except ValueError as e:
    print(f"Warning: Workflow ID '{workflow_id}' is not a valid UUID format")
    print("Please ensure your workflow ID is in the format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

def get_access_token():
    """Get a new access token using JWT authentication"""
    try:
        # Create the JWT assertion
        now = int(time.time())
        payload = {
            "iss": DOCUSIGN_INTEGRATION_KEY,
            "sub": DOCUSIGN_USER_ID,
            "iat": now,
            "exp": now + 3600,  # Token expires in 1 hour
            "aud": "account-d.docusign.com",
            "scope": "signature impersonation"
        }

        # Replace '\n' with actual newlines for PEM format
        pem_private_key = DOCUSIGN_PRIVATE_KEY.replace('\\n', '\n').replace('\n', '\n')

        # Sign the JWT with your private key
        assertion = jwt.encode(
            payload,
            pem_private_key,
            algorithm="RS256"
        )

        # Request the access token
        response = requests.post(
            "https://account-d.docusign.com/oauth/token",
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": assertion
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        raise Exception(f"Failed to get access token: {str(e)}")

def get_api_client():
    """Get an API client with a valid access token"""
    api_client = ApiClient()
    api_client.host = DOCUSIGN_BASE_PATH
    access_token = get_access_token()
    api_client.set_default_header("Authorization", f"Bearer {access_token}")
    return api_client

def create_envelope(signer_email, signer_name, document_path):
    try:
        # Hardcoded workflow ID
        workflow_id = 'c368e411-1592-4001-a3df-dca94ac539ae'
        print("\n=== DocuSign Workflow ID Debug Info ===")
        print("Hardcoded workflow ID:", repr(workflow_id))
        print("Workflow ID length:", len(workflow_id))
        print("Workflow ID type:", type(workflow_id))
        
        # Validate UUID format
        try:
            uuid_obj = uuid.UUID(workflow_id)
            workflow_id = str(uuid_obj)  # Ensure proper UUID format
        except ValueError:
            raise ValueError(f"Invalid workflow ID format: {workflow_id}. Must be a valid UUID.")
        print("Cleaned workflow ID:", repr(workflow_id))
        print("=====================================\n")

        with open(document_path, "rb") as file:
            document_bytes = base64.b64encode(file.read()).decode("utf-8")

        envelope_definition = {
            "emailSubject": "Please sign and verify your identity",
            "documents": [
                {
                    "documentBase64": document_bytes,
                    "name": "Manager Agreement",
                    "fileExtension": "pdf",
                    "documentId": "1"
                }
            ],
            "recipients": {
                "signers": [
                    {
                        "email": signer_email,
                        "name": signer_name,
                        "recipientId": "1",
                        "routingOrder": "1",
                        "clientUserId": "12345",
                        "identityVerification": {
                            "workflowId": workflow_id,
                            "inputOptions": [
                                {
                                    "name": "phone_number_list",
                                    "valueType": "PhoneNumberList",
                                    "phoneNumberList": [
                                        {
                                            "countryCode": "1",
                                            "number": "1234567890"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            "status": "sent"
        }

        print("\n=== Envelope JSON ===")
        print(json.dumps(envelope_definition, indent=2))
        print("=====================\n")

        api_client = get_api_client()
        envelope_api = EnvelopesApi(api_client)
        
        try:
            envelope = envelope_api.create_envelope(
                account_id=DOCUSIGN_ACCOUNT_ID,
                envelope_definition=envelope_definition
            )
            return envelope.envelope_id
        except ApiException as e:
            print("\n=== DocuSign API Error Details ===")
            print("Error Response:", e.body)
            print("Response Headers:", e.headers)
            print("================================\n")
            raise Exception(f"DocuSign API Error: {e.body}")
    except Exception as e:
        raise Exception(f"Error creating envelope: {str(e)}")

def generate_recipient_view(envelope_id, return_url, signer_email, signer_name):
    try:
        view_request = RecipientViewRequest(
            authentication_method="none",
            client_user_id="12345",
            recipient_id="1",
            return_url=return_url,
            user_name=signer_name,
            email=signer_email
        )

        api_client = get_api_client()
        view_url = EnvelopesApi(api_client).create_recipient_view(
            account_id=DOCUSIGN_ACCOUNT_ID,
            envelope_id=envelope_id,
            recipient_view_request=view_request
        )

        return view_url.url
    except ApiException as e:
        raise Exception(f"DocuSign API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating recipient view: {str(e)}")
