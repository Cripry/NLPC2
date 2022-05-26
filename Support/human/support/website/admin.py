from django.contrib import admin

# Register your models here.


from .models import  Custom, Category


admin.site.register(Custom)
admin.site.register(Category)
