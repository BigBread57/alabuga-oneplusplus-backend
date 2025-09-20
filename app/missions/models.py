from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractBaseModel
from apps.gamification.models import Artifact, Competency, Rank


class MissionCategory(models.TextChoices):
    """
    Категории миссий.
    """
    QUEST = 'QUEST', _('Квест')
    RECRUITING = 'RECRUITING', _('Рекрутинг')
    LECTURING = 'LECTURING', _('Лекторий')
    SIMULATOR = 'SIMULATOR', _('Симулятор')


class MissionBranch(AbstractBaseModel):
    """
    Ветка миссий.
    """
    
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
    )
    category = models.CharField(
        verbose_name=_('Категория'),
        max_length=20,
        choices=MissionCategory.choices,
    )
    icon = models.ImageField(
        verbose_name=_('Иконка'),
        upload_to='mission_branches',
        null=True,
        blank=True,
    )
    order = models.IntegerField(
        verbose_name=_('Порядок'),
        default=0,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Ветка миссий')
        verbose_name_plural = _('Ветки миссий')
        ordering = ['category', 'order']
        
    def __str__(self):
        return f'{self.get_category_display()} - {self.name}'


class Mission(AbstractBaseModel):
    """
    Миссия.
    """
    
    name = models.CharField(
        verbose_name=_('Название миссии'),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_('Описание миссии'),
    )
    branch = models.ForeignKey(
        MissionBranch,
        verbose_name=_('Ветка'),
        on_delete=models.CASCADE,
        related_name='missions',
    )
    experience_reward = models.IntegerField(
        verbose_name=_('Награда в опыте'),
        default=0,
    )
    mana_reward = models.IntegerField(
        verbose_name=_('Награда в мане'),
        default=0,
    )
    min_rank = models.ForeignKey(
        Rank,
        verbose_name=_('Минимальный ранг'),
        on_delete=models.PROTECT,
        related_name='available_missions',
        null=True,
        blank=True,
        help_text=_('Минимальный ранг для доступа к миссии'),
    )
    required_missions = models.ManyToManyField(
        'self',
        verbose_name=_('Необходимые миссии'),
        symmetrical=False,
        related_name='unlocks_missions',
        blank=True,
        help_text=_('Миссии, которые нужно выполнить для доступа к этой миссии'),
    )
    artifacts = models.ManyToManyField(
        Artifact,
        verbose_name=_('Награды-артефакты'),
        through='MissionArtifact',
        related_name='missions',
        blank=True,
    )
    order = models.IntegerField(
        verbose_name=_('Порядок в ветке'),
        default=0,
    )
    is_key_mission = models.BooleanField(
        verbose_name=_('Ключевая миссия'),
        default=False,
        help_text=_('Обязательная миссия для получения ранга'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Активна'),
        default=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Миссия')
        verbose_name_plural = _('Миссии')
        ordering = ['branch', 'order']
        
    def __str__(self):
        return self.name


class MissionCompetency(AbstractBaseModel):
    """
    Прокачка компетенций за миссию.
    """
    
    mission = models.ForeignKey(
        Mission,
        verbose_name=_('Миссия'),
        on_delete=models.CASCADE,
        related_name='competencies',
    )
    competency = models.ForeignKey(
        Competency,
        verbose_name=_('Компетенция'),
        on_delete=models.CASCADE,
        related_name='missions',
    )
    points = models.IntegerField(
        verbose_name=_('Очки прокачки'),
        default=1,
        help_text=_('На сколько повысится уровень компетенции'),
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Компетенция миссии')
        verbose_name_plural = _('Компетенции миссий')
        unique_together = ['mission', 'competency']
        
    def __str__(self):
        return f'{self.mission.name} - {self.competency.name}: +{self.points}'


class MissionArtifact(AbstractBaseModel):
    """
    Артефакты за выполнение миссии.
    """
    
    mission = models.ForeignKey(
        Mission,
        verbose_name=_('Миссия'),
        on_delete=models.CASCADE,
    )
    artifact = models.ForeignKey(
        Artifact,
        verbose_name=_('Артефакт'),
        on_delete=models.CASCADE,
    )
    drop_chance = models.FloatField(
        verbose_name=_('Шанс выпадения'),
        default=1.0,
        help_text=_('Вероятность получения артефакта (0.0 - 1.0)'),
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Артефакт миссии')
        verbose_name_plural = _('Артефакты миссий')
        unique_together = ['mission', 'artifact']
        
    def __str__(self):
        return f'{self.mission.name} - {self.artifact.name}'


class RankMission(AbstractBaseModel):
    """
    Обязательные миссии для получения ранга.
    """
    
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Ранг'),
        on_delete=models.CASCADE,
        related_name='required_missions',
    )
    mission = models.ForeignKey(
        Mission,
        verbose_name=_('Миссия'),
        on_delete=models.CASCADE,
        related_name='required_for_ranks',
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Обязательная миссия для ранга')
        verbose_name_plural = _('Обязательные миссии для рангов')
        unique_together = ['rank', 'mission']
        
    def __str__(self):
        return f'{self.rank.name} - {self.mission.name}'


class UserMission(AbstractBaseModel):
    """
    Прогресс пользователя по миссиям.
    """
    
    class Status(models.TextChoices):
        """
        Статус выполнения миссии.
        """
        AVAILABLE = 'AVAILABLE', _('Доступна')
        IN_PROGRESS = 'IN_PROGRESS', _('В процессе')
        COMPLETED = 'COMPLETED', _('Выполнена')
        PENDING_REVIEW = 'PENDING_REVIEW', _('На проверке')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='missions',
    )
    mission = models.ForeignKey(
        Mission,
        verbose_name=_('Миссия'),
        on_delete=models.CASCADE,
        related_name='users',
    )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    started_at = models.DateTimeField(
        verbose_name=_('Начата'),
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        verbose_name=_('Завершена'),
        null=True,
        blank=True,
    )
    result = models.TextField(
        verbose_name=_('Результат'),
        blank=True,
        help_text=_('Результат выполнения миссии (ссылки, файлы и т.д.)'),
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Проверил'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_missions',
    )
    review_comment = models.TextField(
        verbose_name=_('Комментарий проверяющего'),
        blank=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Миссия пользователя')
        verbose_name_plural = _('Миссии пользователей')
        unique_together = ['user', 'mission']
        
    def __str__(self):
        return f'{self.user} - {self.mission.name} ({self.get_status_display()})'
