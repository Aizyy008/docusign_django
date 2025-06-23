from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .docusign_service import create_envelope, generate_recipient_view
import os
from django.shortcuts import render
from django.views.generic import View

class StartSigningPageView(View):
    template_name = 'docusign_app/start_signing.html'

    def get(self, request):
        return render(request, self.template_name)

class StartSigningView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        email = user.email
        name = user.get_full_name() or user.email  # Ensure name is never empty

        document_path = os.path.join(os.path.dirname(__file__), "documents", "contract.pdf")
        return_url = "http://localhost:8000/api/docusign/after-sign"
        envelope_id = create_envelope(email, name, document_path)
        signing_url = generate_recipient_view(envelope_id, return_url, email, name)

        # You can save envelope ID to the DB to track status
        return Response({"signing_url": signing_url})

def after_sign_view(request):
    """
    View to handle the return URL after signing.
    This is where DocuSign will redirect the user after they complete signing.
    """
    # You can add logic here to check the signing status, update your database, etc.
    return render(request, 'docusign_app/signing_complete.html', {
        'message': 'Thank you for signing the document!'
    })
