from rest_framework import serializers

from .models import Bill, MemberOfParliament


class MemberOfParliamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberOfParliament
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"


class BillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ["id", "voting_date", "title"]
