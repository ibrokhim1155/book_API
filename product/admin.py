from django.contrib import admin
from .models import Category, Group, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    search_fields = ('title',)
    list_filter = ('category',)
    ordering = ('title',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'quantity', 'group')
    search_fields = ('title', 'description')
    list_filter = ('group',)
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}
