from django.contrib import admin

from .models import Category, Channel, Server


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'description', 'id')
    list_filter = ('name',)
    search_fields = ['title', 'description']


class ServerAdmin(admin.ModelAdmin):
    model = Server
    list_display = ('name', 'owner', 'category', 'description')
    list_filter = ('name', 'owner', 'category')
    search_fields = ['title', 'description', 'category']


class ChannelAdmin(admin.ModelAdmin):
    model = Channel
    list_display = ('name', 'owner', 'topic', 'server')
    list_filter = ('name', 'owner', 'topic', 'server')
    search_fields = ['name', 'topic', 'server']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Channel, ChannelAdmin)
