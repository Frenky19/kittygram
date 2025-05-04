from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat
from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с кошками."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Устанавливает текущего пользователя как владельца кошки."""
        serializer.save(owner=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    """ViewSet для управления достижениями."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None
