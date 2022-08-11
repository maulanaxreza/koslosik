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
    path('penyewaan',views.penyewaan,name='penyewaan'),
    path('sewa',views.sewa,name='sewa'),
    path('cek',views.cek,name='cek'),
    path('adddetailcharge',views.inputcharge,name='adddetailcharge'),
    path('checkout/<str:id>',views.checkout,name='checkout'),
    path('detailcharge/<str:id>/view',views.detailcharge,name='detailcharge'),
    path('laporan',views.laporan,name='laporan'),
    path('laporanpdf/<str:mulai>/<str:akhir>',views.laporanpdf,name='laporanpdf'),
    path('notapdf/<str:id>/',views.notapdf,name='notapdf'),
    path('pdf',views.pdfgen)

]
