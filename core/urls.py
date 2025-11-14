from django.urls import path
from .views import HomeView, produtos, servicos, adocao

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('produtos/', produtos, name='produtos'),
    path('servicos/', servicos, name='servicos'),
    path('adocao/', adocao, name='adocao'),
]