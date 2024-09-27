from django.contrib import admin
from django.utils import timezone
from .models import Category, Group, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'slug')
    search_fields = ('title',)
    list_filter = ('category',)
    ordering = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'quantity', 'group', 'is_active')  # is_active qo'shildi
    search_fields = ('title', 'description')
    list_filter = ('group', 'is_active')  # is_active qo'shildi
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'discount', 'quantity', 'group', 'is_active', 'slug')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)
