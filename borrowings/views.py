from datetime import datetime

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from books.models import Book
from borrowings.models import Borrowing, Payment
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer,
    BorrowingPostSerializer, BorrowingReturnSerializer, PaymentSerializer
)
from utilities.send_telegram_message import send_tg_message
from utilities.stripe_helper import stripe_helper


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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        book.inventory = book.inventory - 1
        book.save()
        borrowing_id = serializer.data.get("id")
        borrowing = Borrowing.objects.get(id=borrowing_id)
        stripe_helper(borrowing)
        send_tg_message(
            f"You successfully borrowed {book.title}.\n"
            f"Detail info:\n"
            f"Borrow date is {borrowing.borrow_date}\n"
            f"Return book at: {borrowing.expected_return_date}\n"
            f"Daily fee is {borrowing.book.daily_fee} USD$"
        )
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
        with transaction.atomic():
            if borrowing.user == self.request.user:
                borrowing.book.inventory += 1
                borrowing.actual_return_date = datetime.now()
                borrowing.save()
                send_tg_message(f"Your book:{borrowing.book} has been successfully returned")
                return Response({"message": "Borrowing successfully returned"}, status=status.HTTP_200_OK)
        return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = Payment.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(borrowing__user=self.request.user)
        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="success"
    )
    def success(self, request, pk=None):
        return Response(
            {"message": "Payment success"},
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["get"],
        url_path="cancel"
    )
    def cancel(self, request, pk=None):
        return Response(
            {"message": "Payment cancelled"},
            status=status.HTTP_200_OK
        )
