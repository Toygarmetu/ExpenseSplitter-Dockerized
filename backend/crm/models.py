from django.db import models

from django.shortcuts import render
from backend.models import ExpenseGroup
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ExpenseGroup(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backend_expensegroups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backend_expenses_payer')
    participants = models.ManyToManyField(User, related_name='backend_expenses_participants')
    group = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE, related_name='backend_expenses')

    def __str__(self):
        return self.title