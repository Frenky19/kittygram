from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Achievement(models.Model):
    """
    Модель для представления достижений кошек.

    Attributes:
        name (CharField): Название достижения. Максимальная длина 64 символа.
    """

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    """
    Модель для представления кошек.

    Attributes:
        name (CharField): Кличка кошки. Максимальная длина 16 символов.
        color (CharField): Окрас кошки. Максимальная длина 16 символов.
        birth_year (IntegerField): Год рождения кошки.
        owner (ForeignKey): Владелец кошки. Связь с моделью User.
        achievements (ManyToManyField): Достижения кошки через промежуточную
            модель AchievementCat.
        image (ImageField): Фотография кошки. Сохраняется в cats/images/.

    Relationships:
        - Связь с пользователем: одна кошка → один владелец
        - Связь с достижениями: много-ко-много через AchievementCat
    """

    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    achievements = models.ManyToManyField(Achievement,
                                          through='AchievementCat')
    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    """
    Промежуточная модель для связи кошек и их достижений.

    Attributes:
        achievement (ForeignKey): Ссылка на достижение
        cat (ForeignKey): Ссылка на кошку

    Note:
        Создается автоматически при добавлении достижений кошке через
            ManyToManyField.
    """

    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'
