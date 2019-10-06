from django.contrib import admin

# Register your models here.

from . models import user_reg, Category, Product, Subcategories

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['Scategory', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category','subcategory', 'price', 'discount', 'stock', 'available', 'created', 'update']
    list_filter = ['available', 'created', 'update' ,'category']
    list_editable = ['price', 'discount', 'stock', 'available', ]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(user_reg)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Subcategories, SubCategoryAdmin)

