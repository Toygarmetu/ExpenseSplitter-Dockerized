from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from backend.models import ExpenseGroup
from .models import ExpenseGroup
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import ExpenseGroup, Expense
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Group
from django.views.generic import ListView
from .models import Expense
from .forms import ExpenseForm


# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView
from django.core.exceptions import ValidationError


def homepage(request):

    return render(request, 'crm/index.html')




def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my-login")


    context = {'registerform':form}

    return render(request, 'crm/register.html', context=context)



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("")



@login_required(login_url="my-login")
def dashboard(request):
    expense_groups = ExpenseGroup.objects.filter(created_by=request.user)
    return render(request, 'crm/dashboard.html', {'expense_groups': expense_groups})

class ExpenseGroupDetailView(DetailView):
    model = ExpenseGroup
    template_name = 'group_detail.html'


class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseGroup
    fields = ['name']
    template_name = 'crm/expensegroup_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseGroup
    fields = ['name']
    template_name = 'crm/expensegroup_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['expense_form'] = ExpenseForm()
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.group_id = self.kwargs['group_id']
        response = super().form_valid(form)

        # Create an Expense instance
        expense = Expense()
        expense.title = self.request.POST.get('expense_title')
        expense.amount = self.request.POST.get('expense_amount')
        expense.date = self.request.POST.get('expense_date')
        expense.payer = User.objects.get(id=self.request.POST.get('expense_payer'))
        expense.group = self.object  # Associate the expense with the newly created group
        expense.save()

        # Add participants to the expense
        participant_ids = self.request.POST.getlist('expense_participants')
        for participant_id in participant_ids:
            participant = User.objects.get(id=participant_id)
            expense.participants.add(participant)

        return response

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.kwargs['group_id']})
    
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['title', 'amount', 'date', 'payer']  # replace with your actual fields
    template_name = 'crm/expense_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        try:
            form.instance.payer = User.objects.get(id=self.request.POST.get('expense_payer'))
        except User.DoesNotExist:
            form.add_error('payer', ValidationError('User with this ID does not exist.'))
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class ExpenseGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseGroup
    fields = ['name']
    template_name = 'crm/expensegroup_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    
class DashboardView(ListView):
    model = ExpenseGroup
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context