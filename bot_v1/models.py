from django.db import models

class BotUser(models.Model):
    user_id = models.PositiveIntegerField(unique=True, verbose_name='ID пользователя')
    search_history = models.ForeignKey('SearchHistory',
                        verbose_name='История поиска', blank = True, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.user_id} {self.search_history}'

    class Meta:
        verbose_name = 'Пользователь Бота'
        verbose_name_plural = 'Пользователи'

class SearchArea(models.Model):
    name = models.TextField(verbose_name='Область поиска')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область поиска'
        verbose_name_plural = 'Области поиска'


class SearchHistory(models.Model):
    req = models.TextField(verbose_name='Запрос')
    result = models.TextField(verbose_name='Результат')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')

    def __str__(self):
        return 'По вашему запросу: "%s" найдены следуйщие результаты %s' % (self.req, self.result)

    class Meta:
        verbose_name = 'История поиска'
        verbose_name_plural = 'Истории поисков'
