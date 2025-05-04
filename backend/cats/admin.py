from django.contrib import admin

from .models import Achievement, AchievementCat, Cat


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Achievement.

    Позволяет просматривать и управлять достижениями кошек.

    Attributes:
        list_display (tuple): Отображаемые поля в списке (id, название)
        list_display_links (tuple): Поля-ссылки для редактирования (название)
        search_fields (tuple): Поля для поиска (название)
    """

    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Cat.

    Управление профилями кошек с расширенными возможностями.

    Attributes:
        list_display (tuple): Отображаемые поля в списке
        list_filter (tuple): Поля для фильтрации справа
        search_fields (tuple): Поля для поиска
        filter_horizontal (tuple): Виджет для выбора достижений
    """

    list_display = (
        'name',
        'color',
        'birth_year',
        'owner',
        'image',
    )
    list_filter = ('color', 'birth_year', 'owner')
    search_fields = ('name', 'owner__username')
    filter_horizontal = ('achievements',)


@admin.register(AchievementCat)
class AchievementCatAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для промежуточной модели AchievementCat.

    Управление связями между кошками и их достижениями.

    Attributes:
        list_display (tuple): Отображаемые поля в списке
        list_filter (tuple): Поля для фильтрации
        search_fields (tuple): Поля для поиска по связанным моделям
    """

    list_display = ('id', 'achievement', 'cat')
    list_filter = ('achievement', 'cat')
    search_fields = (
        'achievement__name',
        'cat__name',
        'cat__owner__username'
    )
