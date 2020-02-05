from django.urls import path

from . import views

app_name = 'story'
urlpatterns = [
#        path('', views.IndexView.as_view(), name='index'),
        path('<int:pk>/',views.DetailView.as_view(),name='detail'),
        path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),

        path('', views.index, name='index'),
        path('logingin', views.logingin, name="logingin"),
        path('logout', views.logout_view, name="logout"),
        path('login', views.login_view, name="login"),
        path('register', views.register, name="register"),
        path('registering', views.registering, name="registering"),
        path('wish', views.wish, name="wish"),
        path('wishing', views.wishing, name="wishing"),
        path('wish/<int:wish_id>/', views.wish_detail, name="wish_detail"),
        path('wish/<int:wish_id>/edit/', views.wish_edit, name="wish_edit"),
        path('wish/editing/', views.wish_editing, name="wish_editing"),

        path('projects/', views.projects, name="projects"),
        path('projects/<int:project_id>/', views.project_detail, name="project_detail"),
        path('wishwall/', views.wishwall,name="wishwall"),
        ]
