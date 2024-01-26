from datetime import datetime
from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from .models import User

from .serializers import UserSerializer, UserDetailSerializer

FIFTEEN_YEARS_IN_DAYS = 15 * 365.25


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()

    @transaction.atomic
    def create(self, request):
        age_str = request.data['age']

        if age_str:
            try:
                age_date = datetime.strptime(age_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Format de date invalide. Utilisez le format YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data['age'] = age_date

        if age_date:
            fifteen_years_ago = timezone.now() - timezone.timedelta(days=FIFTEEN_YEARS_IN_DAYS)
            is_under_fifteen = age_date >= fifteen_years_ago.date()

            if is_under_fifteen:
                request.data['can_data_be_shared'] = not is_under_fifteen

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = User.objects.get(pk=serializer.data['id'])
        user.set_password(serializer.data['password'])
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
