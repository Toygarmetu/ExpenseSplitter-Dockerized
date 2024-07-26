from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import ExpenseGroup
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import ExpenseGroup, Expense
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

@api_view(['GET'])
def send_some_data(request):
    return Response({
        "data": "Hello from django backend"
    })
    

class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseGroup
    fields = ['name']
    template_name = 'expensegroup_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['title', 'amount', 'date', 'payer', 'participants']
    template_name = 'expense_form.html'

    def get_form(self):
        form = super().get_form()
        form.fields['payer'].queryset = User.objects.all()
        form.fields['participants'].queryset = User.objects.all()
        return form

    def form_valid(self, form):
        form.instance.group_id = self.kwargs['group_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.kwargs['group_id']})

@login_required
def dashboard(request):
    expense_groups = ExpenseGroup.objects.filter(created_by=request.user)
    return render(request, 'crm/dashboard.html', {'expense_groups': expense_groups})