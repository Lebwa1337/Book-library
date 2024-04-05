from django.urls import path

from borrowings.views import BorrowingsViewSet

urlpatterns = [
    path("", BorrowingsViewSet.as_view(), name="borrow")
]


app_name = "borrowings"
