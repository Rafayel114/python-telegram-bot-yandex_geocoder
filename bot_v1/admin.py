from django.contrib import admin

from .models import *


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'search_history')


@admin.register(SearchArea)
class SearchAreaAdmin(admin.ModelAdmin):
    display = 'name'


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('req', 'result', 'date')
