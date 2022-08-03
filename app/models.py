from django.db import models

# Create your models here.
class pelanggan(models.Model):
    idpelanggan = models.CharField(max_length=5, primary_key=True)
    nama = models.CharField(max_length=50)
    jeniskelamin = models.CharField(max_length=10)
    tanggallahir = models.DateField()
    nohp = models.IntegerField()

    def __str__(self):
        return self.nama

class kamar (models.Model):
    idkamar = models.CharField(max_length=5, primary_key=True)
    nokamar = models.IntegerField()
    jenis = models.CharField(max_length=15, default='laki-laki')
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nokamar) + ' - ' + str(self.jenis)

class charge(models.Model):
    idcharge = models.CharField(max_length=5, primary_key=True)
    jenischarge = models.CharField(max_length=50)
    hargacharge = models.IntegerField()

    def __str__(self):
        return self.jenischarge

class penyewaan(models.Model):
    idpenyewaan = models.CharField(primary_key=True, max_length=5)
    idpelanggan = models.ForeignKey(pelanggan,on_delete=models.CASCADE)
    idkamar = models.OneToOneField(kamar,on_delete=models.CASCADE)
    tanggalsewa = models.DateField()
    hargasewa = models.IntegerField()

    def __str__(self):
        return str(self.idpelanggan) 

class detailcharge(models.Model):
    iddetailcharge = models.CharField(max_length=5, primary_key=True)
    idpelanggan = models.ForeignKey(pelanggan,on_delete=models.CASCADE,null=True)
    idcharge = models.ForeignKey(charge,on_delete=models.CASCADE)
    jumlahitemcharge = models.IntegerField()
    hargacharge = models.IntegerField()

    def __str__(self):
        return self.iddetailcharge
