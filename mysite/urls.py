"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beta import views as beta_views
from cloudpharma import views as cloudpharma_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', beta_views.login_user),
    path('create_user/', beta_views.create_user),
    path('delete_user/', beta_views.delete_user),
    path('changeemail/', beta_views.update_email),
    path('changepassword/', beta_views.update_password),
    path('recoverpassword/', beta_views.forgot_password),
    path('logout/', beta_views.logout_user),
    path('check_auth/', beta_views.check_auth),
    path('get_user/', beta_views.get_user),
    path('subscription/', beta_views.create_subscription),
    path('deletesubscription/', beta_views.delete_subscription),
    path('validate-payment/', beta_views.validate_stripe_payment),
    path('contact/', beta_views.contact),
    path('validate-password-token/', beta_views.validadte_password_token),
    path('get-meds/',   cloudpharma_views.get_meds),
    path('create-med/', cloudpharma_views.create_med),
    path('update-med/',  cloudpharma_views.update_med),
    path('delete-med/',  cloudpharma_views.delete_med)
]
