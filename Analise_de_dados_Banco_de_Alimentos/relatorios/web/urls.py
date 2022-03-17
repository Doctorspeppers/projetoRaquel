from django.urls import include, path
from . import views

urlpatterns = [
    path('relatorio/<str:id>', views.relatorio_colheita),
]