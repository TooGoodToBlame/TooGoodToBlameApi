from rest_framework import serializers

from .models import Bill, MemberOfParliament, Vote


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


class BillWithMPVoteSerializer(serializers.ModelSerializer):
    """
    Serializer używany w widoku MemberOfParliamentBills.
    Zwraca podstawowe informacje o ustawie oraz głos konkretnego parlamentarzysty (mp_vote).
    """
    mp_vote = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = [
            "id",
            "voting_date",
            "title",
            "mp_vote",
        ]

    def get_mp_vote(self, obj):
        """
        Zwraca głos konkretnego parlamentarzysty (z widoku)
        dla danej ustawy (Bill).
        """
        mp_id = self.context.get("mp_id")
        if not mp_id:
            return None

        # Szukamy głosu w tabeli Vote
        vote_instance = Vote.objects.filter(
            bill=obj,
            member_of_parliament_id=mp_id
        ).first()

        if vote_instance:
            # Zwracamy pełną nazwę głosu: "Za", "Przeciw", "Wstzymany"
            return vote_instance.get_vote_display()
            # Jeśli zamiast nazwy chcesz jedynie literkę (Z/P/W), użyj:
            # return vote_instance.vote
        return None


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer do wyświetlania głosu konkretnego MemberOfParliament
    (z danymi o samym parlamentarzyście i rodzajem głosu).
    """
    member_of_parliament = MemberOfParliamentSerializer(read_only=True)
    # Zamiast krótkiego pola (Z/P/W) możesz zwrócić label głosu:
    vote_label = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = [
            "id",
            "member_of_parliament",
            "vote",        # skrót (Z/P/W)
            "vote_label",  # pełna nazwa (Za/Przeciw/Wstzymany)
        ]

    def get_vote_label(self, obj):
        return obj.get_vote_display()
