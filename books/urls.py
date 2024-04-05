from django.urls import path, include
from rest_framework import routers

from books.views import BooksViewSet

router = routers.DefaultRouter()
router.register("books", BooksViewSet)
urlpatterns = [
    path("", include(router.urls))
]


app_name = 'books'
