from django.urls import path,re_path
from . import views

app_name = 'user'

urlpatterns = [

    path('signin', view=views.ObtainAuthToken.as_view(), name='signin'),
    path('signout', views.Signout.as_view(), name='signout'),
    path(r'new-user', views.NewUserView.as_view(),  name='new_user'),
    path(r'upload-file', views.UploadFileView.as_view(),  name='upload_file'),
    path(r'get-progress', views.GetProgress.as_view(),  name='get_progress'),



]