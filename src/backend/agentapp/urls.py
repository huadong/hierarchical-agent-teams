from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('question', views.question, name='question'),
    path('graph', views.graph, name='graph'),
    # re_path(r'uploads/.*', views.uploads),
    # path('ocr', views.ocr, name='ocr'),
    # path('gpt', views.gpt, name='gpt'),
    # path('transform', views.transform, name='transform'),
]