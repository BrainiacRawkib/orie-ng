from django.contrib import admin
from .models import Category, Product, Review, ProductImages


class ProductImagesInline(admin.TabularInline):
    model = ProductImages


class ProductReviewInline(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'merchant', 'price', 'available', 'date_added', 'updated']
    list_display_links = ['name']
    list_editable = ['price', 'available']
    search_fields = ['name', 'category', 'merchant', 'price', 'available']
    raw_id_fields = ['category', 'merchant']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    inlines = [ProductImagesInline, ProductReviewInline]


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'ratings', 'created']
    list_display_links = ['product']
    readonly_fields = ['product', 'author', 'ratings', 'comment', 'created']
