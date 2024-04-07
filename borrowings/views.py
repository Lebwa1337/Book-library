from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingPostSerializer, BorrowingReturnSerializer
)


class BorrowingsViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "create":
            return BorrowingPostSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        book.inventory = book.inventory - 1
        book.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        if is_active == "1":
            queryset = queryset.filter(actual_return_date=None)
        if user_id and self.request.user.is_staff:
            queryset = queryset.filter(user_id=int(user_id))
        return queryset


class ReturnBorrowing(CreateAPIView):
    serializer_class = BorrowingReturnSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        borrowing_id = self.request.data.get("borrowing_id")
        borrowing = Borrowing.objects.get(id=borrowing_id)
        if borrowing.actual_return_date:
            raise PermissionError("This book was already returned")
        if borrowing.user == self.request.user:
            borrowing.book.inventory += 1
            borrowing.actual_return_date = datetime.now()
            borrowing.save()
        return Response({"message": "Borrowing successfully returned"}, status=status.HTTP_200_OK)
