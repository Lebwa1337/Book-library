from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        ]


class PaymentBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "status",
            "type",
            "session_url",
            "session_id",
            "money_to_pay"
        ]


class BorrowingSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(read_only=True)
    payment = PaymentBorrowSerializer(read_only=True, many=True)

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payment"
        ]


class BorrowingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "book",
        ]


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.CharField(source="book.title", read_only=True)
    user = serializers.CharField(source="user.email", read_only=True)


class BorrowingDetailSerializer(BorrowingListSerializer):
    book = BookSerializer(read_only=True)


class BorrowingReturnSerializer(serializers.Serializer):
    borrowing_id = serializers.IntegerField()
