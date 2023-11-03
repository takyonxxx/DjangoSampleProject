from django.db import models, transaction


class TestSubModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tbl_test_sub_model'


class TestModel(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    #  many-to-one relationship
    sub_model = models.ForeignKey(TestSubModel, related_name='test_models',
                                  null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'tbl_test_model'

    def __str__(self):
        return f"{self.name} ({self.age} years old)"


# Base Class
class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()


# Multi-table Inheritance
class Employee(Person):
    position = models.CharField(max_length=100)


# Proxy Model
class ManagerProxy(Person):
    class Meta:
        proxy = True


# Abstract Base Class
class CommonFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Model 1
class Article(CommonFields):
    title = models.CharField(max_length=100)
    content = models.TextField()


# Model 2
class Comment(CommonFields):
    author = models.CharField(max_length=50)
    text = models.TextField()
