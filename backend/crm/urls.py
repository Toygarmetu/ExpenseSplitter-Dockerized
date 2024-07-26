from django.urls import path

from . import views

urlpatterns = [

    path('', views.homepage, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user_logout"),
    
    
    path('group/<int:pk>/', views.ExpenseGroupDetailView.as_view(), name='group_detail'),
    
    path('group/<int:pk>/update/', views.ExpenseGroupUpdateView.as_view(), name='group_update'),
    
    path('expense/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    
    path('expensegroup/create/<int:group_id>/', views.ExpenseGroupCreateView.as_view(), name='expensegroup_create'),
]










