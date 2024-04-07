from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
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
