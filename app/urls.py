from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("", views.home, name="home"),
    path("negociations/", views.negociations, name="negociations"),

    path("", include("brokers.urls")),
    path("", include("tickers.urls")),
    path("", include("inflows.urls")),
    path("", include("outflows.urls")),
    path("", include("dividends.urls")),
]

# Custom error handlers
handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
