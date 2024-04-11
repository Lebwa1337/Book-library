from django.urls import path, include
from rest_framework import routers

from borrowings.views import (
    BorrowingsViewSet,
    ReturnBorrowing,
    PaymentViewSet
)

router = routers.DefaultRouter()
router.register("borrowings", BorrowingsViewSet)
router.register("payments", PaymentViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("borrowings-return/", ReturnBorrowing.as_view(), name="return_borrowing"),

]


app_name = "borrowings"
