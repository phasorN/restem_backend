from django.contrib import admin
from django.urls import path
from django.urls import include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('', views.api_root),
    path('users/', views.UserSelfDetailsOrCreate.as_view(), name="user-list"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path('expenses/', views.ExpensesList.as_view(), name="expenses-list"),
    path('expenses/<int:pk>/', views.ExpensesDetail.as_view(), name="expenses-detail"),
]

