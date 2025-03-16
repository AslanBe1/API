from django.contrib import admin

from api.models import Product, Category, Comment


# Register your models here.

@admin.register(Product)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Comment)