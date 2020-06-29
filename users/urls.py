from django.urls import path
from .views import UpdateUserView, GetProfileDataView

urlpatterns = [
    path('update/', UpdateUserView.as_view()),
    path('get_profile/', GetProfileDataView.as_view()),
]
