from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [

    # student
    path('student/class/', views.ClassShow.as_view(), name='STU_show_classes'),
    path('student/class-detail/<int:pk>', views.ClassDetail.as_view(), name='STU_class_detail'),
    path('student/select-classes/', views.SelectClass.as_view(), name='STU_select_classes'),
    path('student/select-class/<int:pk>', views.SelectClassLesson, name='STU_select_class'),
    path('student/rented-book/', views.RentedBook.as_view(), name='STU_show_rented_book'),
]
