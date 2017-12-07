from django.conf.urls import url
from questions import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^question01$', views.question_01, name='question_01'),
    url(r'^question02$', views.question_02, name='question_02'),
	url(r'^question03$', views.question_03, name='question_03'),
    url(r'^question04$', views.question_04, name='question_04'),
    url(r'^question04$', views.question_04, name='question_05'),
] 