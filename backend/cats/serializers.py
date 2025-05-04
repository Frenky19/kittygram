import base64
import datetime as dt

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat


class Hex2NameColor(serializers.Field):
    """Кастомное поле для преобразования HEX-кода цвета в название цвета.

    Особенности:
    - При вводе принимает HEX-формат (например, #ff0000)
    - При выводе возвращает название цвета (например, 'red')
    - Использует библиотеку webcolors для конвертации

    Исключения:
    - ValidationError: если цвет не найден в CSS3-палитре
    """

    def to_representation(self, value):
        """Возвращает исходное значение (название цвета) для API response."""
        return value

    def to_internal_value(self, data):
        """Конвертирует HEX-код в название цвета перед сохранением."""
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Achievement с переименованным полем."""

    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для обработки изображений в формате base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cat.

    Особенности:
    - Динамическое поле 'age' (вычисляется из года рождения)
    - Поддержка base64 для загрузки изображений
    - Кастомная обработка достижений через nested serializer
    - Преобразование цвета через Hex2NameColor

    Поля:
    - image_url: URL загруженного изображения (read-only)
    - achievements: список достижений через AchievementSerializer
    - owner: устанавливается автоматически из контекста запроса
    """

    achievements = AchievementSerializer(required=False, many=True)
    color = Hex2NameColor()
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Cat
        fields = (
            'id', 'name', 'color', 'birth_year', 'achievements',
            'owner', 'age', 'image', 'image_url'
        )
        read_only_fields = ('owner',)

    def get_image_url(self, obj):
        """Генерирует абсолютный URL для изображения."""
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj):
        """Вычисляет возраст кошки на основе года рождения."""
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        """
        Создание кошки с обработкой достижений.

        Логика:
        - Если достижения не переданы - создает простую запись
        - При наличии достижений создает связи через AchievementCat
        - Обрабатывает существующие/новые достижения
        """
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        achievements = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat
            )
        return cat

    def update(self, instance, validated_data):
        """
        Обновление кошки с полной заменой достижений.

        Особенности:
        - Поле achievements полностью перезаписывается
        - Изображение обновляется только при передаче нового
        """
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get(
            'birth_year', instance.birth_year
        )
        instance.image = validated_data.get('image', instance.image)

        if 'achievements' not in validated_data:
            instance.save()
            return instance

        achievements_data = validated_data.pop('achievements')
        lst = []
        for achievement in achievements_data:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement
            )
            lst.append(current_achievement)
        instance.achievements.set(lst)

        instance.save()
        return instance
