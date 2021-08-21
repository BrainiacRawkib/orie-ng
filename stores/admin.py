from django.contrib import admin
from .models import Category, Product, Review


class ProductReviewInline(admin.TabularInline):
    """
    Register Review model on the same page with its associated Product.
    """
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Register Category model in the admin site."""

    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Register Product model in the admin site."""

    list_display = ['name', 'category', 'merchant', 'price', 'stocks_left', 'available', 'date_added', 'updated']
    list_display_links = ['name']
    list_editable = ['price', 'stocks_left', 'available']
    search_fields = ['name', 'category', 'merchant', 'price', 'available']
    raw_id_fields = ['category', 'merchant']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    inlines = [ProductReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Register Review model in the admin site."""

    list_display = ['product', 'author', 'ratings', 'created']
    list_display_links = ['product']
    readonly_fields = ['product', 'author', 'ratings', 'comment', 'created']
