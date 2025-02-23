from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']
        default_related_name = 'comments'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор, на которого подписаны'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_follow')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}'
