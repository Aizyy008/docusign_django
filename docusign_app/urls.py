from django.urls import path
from .views import StartSigningView, after_sign_view, StartSigningPageView

app_name = 'docusign_app'

urlpatterns = [
    path("", StartSigningPageView.as_view(), name="start-signing-page"),
    path("start-signing/", StartSigningView.as_view(), name="start-signing"),
    path("after-sign/", after_sign_view, name="after-sign"),
]
