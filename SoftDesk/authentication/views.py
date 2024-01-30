from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from .models import User

from .serializers import UserSerializer, UserDetailSerializer

from .permissions import UserPermission

FIFTEEN_YEARS = 15


class MultipleSerializerMixin:
    '''Mixin that allows to use different serializers for different actions.'''

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class UserViewSet(MultipleSerializerMixin, ModelViewSet):
    '''Viewset for User model.'''

    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        return User.objects.all()

    @transaction.atomic
    def create(self, request):
        age_str = request.data['age']

        if age_str:
            try:
                age_date = parse_date(age_str).date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data['age'] = age_date

        if age_date:
            fifteen_years_ago = timezone.now() - relativedelta(years=FIFTEEN_YEARS)
            is_under_fifteen = age_date >= fifteen_years_ago.date()

            if is_under_fifteen:
                return Response(
                    {"error": "You must be at least 15 years old to register."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            user = User.objects.get(pk=serializer.data['id'])
            user.set_password(serializer.data['password'])
            user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        age_str = request.data['age']

        if age_str:
            try:
                age_date = parse_date(age_str).date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data['age'] = age_date

        if age_date:
            fifteen_years_ago = timezone.now() - relativedelta(years=FIFTEEN_YEARS)
            is_under_fifteen = age_date >= fifteen_years_ago.date()

            if is_under_fifteen:
                return Response(
                    {"error": "You must be at least 15 years old to use this app."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return super().update(request, *args, **kwargs)
