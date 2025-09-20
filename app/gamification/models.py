from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractBaseModel


class Competency(AbstractBaseModel):
    """
    Компетенция.
    """
    
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
    )
    icon = models.ImageField(
        verbose_name=_('Иконка'),
        upload_to='competencies',
        null=True,
        blank=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Компетенция')
        verbose_name_plural = _('Компетенции')
        
    def __str__(self):
        return self.name


class Rank(AbstractBaseModel):
    """
    Ранг пользователя.
    """
    
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
    )
    order = models.IntegerField(
        verbose_name=_('Порядок'),
        default=0,
        help_text=_('Порядковый номер ранга в иерархии'),
    )
    experience_required = models.IntegerField(
        verbose_name=_('Требуемый опыт'),
        default=0,
        help_text=_('Минимальное количество опыта для получения ранга'),
    )
    icon = models.ImageField(
        verbose_name=_('Иконка'),
        upload_to='ranks',
        null=True,
        blank=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Ранг')
        verbose_name_plural = _('Ранги')
        ordering = ['order']
        
    def __str__(self):
        return self.name


class RankCompetencyRequirement(AbstractBaseModel):
    """
    Требования к компетенциям для получения ранга.
    """
    
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Ранг'),
        on_delete=models.CASCADE,
        related_name='competency_requirements',
    )
    competency = models.ForeignKey(
        Competency,
        verbose_name=_('Компетенция'),
        on_delete=models.CASCADE,
        related_name='rank_requirements',
    )
    level_required = models.IntegerField(
        verbose_name=_('Требуемый уровень'),
        default=1,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Требование к компетенции')
        verbose_name_plural = _('Требования к компетенциям')
        unique_together = ['rank', 'competency']
        
    def __str__(self):
        return f'{self.rank.name} - {self.competency.name}: {self.level_required}'


class UserRank(AbstractBaseModel):
    """
    Текущий ранг пользователя.
    """
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='user_rank',
    )
    rank = models.ForeignKey(
        Rank,
        verbose_name=_('Ранг'),
        on_delete=models.PROTECT,
        related_name='users',
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Ранг пользователя')
        verbose_name_plural = _('Ранги пользователей')
        
    def __str__(self):
        return f'{self.user} - {self.rank}'


class UserCompetency(AbstractBaseModel):
    """
    Уровень компетенции пользователя.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='competencies',
    )
    competency = models.ForeignKey(
        Competency,
        verbose_name=_('Компетенция'),
        on_delete=models.CASCADE,
        related_name='user_levels',
    )
    level = models.IntegerField(
        verbose_name=_('Уровень'),
        default=0,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Компетенция пользователя')
        verbose_name_plural = _('Компетенции пользователей')
        unique_together = ['user', 'competency']
        
    def __str__(self):
        return f'{self.user} - {self.competency.name}: {self.level}'


class Artifact(AbstractBaseModel):
    """
    Артефакт.
    """
    
    class Rarities(models.TextChoices):
        """
        Редкость артефакта
        """
        COMMON = 'COMMON', _("Обычный")
        UNCOMMON = 'UNCOMMON', _("Необычный")
        RARE = 'RARE', _("Редкий")
        EPIC = 'EPIC', _("Эпический")
        LEGEND = 'LEGEND', _("Легендарный")

    media = models.ImageField(
        verbose_name=_('Медиа'),
        upload_to='artifacts',
        blank=True,
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        blank=True,
    )
    rarity = models.CharField(
        verbose_name=_('Редкость'),
        max_length=20,
        choices=Rarities.choices,
        default=Rarities.COMMON,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Артефакт')
        verbose_name_plural = _('Артефакты')

    def __str__(self):
        return self.name


class UserArtifact(AbstractBaseModel):
    """
    Артефакты пользователя.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='artifacts',
    )
    artifact = models.ForeignKey(
        Artifact,
        verbose_name=_('Артефакт'),
        on_delete=models.CASCADE,
        related_name='owners',
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Артефакт пользователя')
        verbose_name_plural = _('Артефакты пользователей')
        unique_together = ['user', 'artifact']
        
    def __str__(self):
        return f'{self.user} - {self.artifact.name}'


class BoardingStep(AbstractBaseModel):
    """
    Шаг онбординга.
    """
    
    title = models.CharField(
        verbose_name=_('Заголовок'),
        max_length=256,
    )
    content = models.TextField(
        verbose_name=_('Контент'),
        help_text=_('Интересные факты о космосе и платформе'),
    )
    order = models.IntegerField(
        verbose_name=_('Порядок'),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен'),
        default=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Шаг онбординга')
        verbose_name_plural = _('Шаги онбординга')
        ordering = ['order']
        
    def __str__(self):
        return self.title


class UserBoardingProgress(AbstractBaseModel):
    """
    Прогресс пользователя в онбординге.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='boarding_progress',
    )
    step = models.ForeignKey(
        BoardingStep,
        verbose_name=_('Шаг'),
        on_delete=models.CASCADE,
        related_name='user_progress',
    )
    completed_at = models.DateTimeField(
        verbose_name=_('Завершен'),
        null=True,
        blank=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Прогресс онбординга')
        verbose_name_plural = _('Прогресс онбординга')
        unique_together = ['user', 'step']
        
    def __str__(self):
        return f'{self.user} - {self.step.title}'
