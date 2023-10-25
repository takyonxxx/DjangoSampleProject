from django.contrib import admin
from .models import TestSubModel, TestModel


class TestSubModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(TestSubModel, TestSubModelAdmin)


class TestModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sub_model')


admin.site.register(TestModel, TestModelAdmin)
