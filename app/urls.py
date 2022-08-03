from django.urls import path
from . import views

urlpatterns = [
    
    path('home',views.dashboard,name='dashboard'),
    path('kamar',views.kamar,name='kamar'),
    path('charge',views.charge,name='charge'),
    path('charge/add',views.addcharge,name='addcharge'),
    path('pelanggan',views.pelanggan,name='pelanggan'),
    path('pelanggan/<str:id>/update',views.updatepelanggan, name="updatepelanggan"),
    path('pelanggan/<str:id>/delete',views.deletepelanggan, name="deletepelanggan"),
    path('sewa',views.sewa,name='sewa'),
    path('cek',views.cek,name='cek'),
    path('adddetailcharge',views.inputcharge,name='adddetailcharge')

]
