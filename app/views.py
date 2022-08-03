from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import models

# Create your views here.

def dashboard(request):
    # Kamar tersedia laki-laki
    kamartersediapa = models.kamar.objects.filter(status = False, jenis = 'laki-laki').count()
    # kamar tersedia perempuan
    kamartersediapi = models.kamar.objects.filter(status = False, jenis = "perempuan").count()
    # Total Pemesanan  
    totalpesan = models.penyewaan.objects.all().count()
    # Total tambah charge


    return render(request,'index.html',{
        'kamartersediapa' : kamartersediapa,
        'kamarterserdiapi' : kamartersediapi,
        'totalpemesanan' : totalpesan,

    })

def kamar(request):
    # get kamar
    kamarobj = models.kamar.objects.all()
    return render(request,'kamar.html',{
        'kamar':kamarobj
    })

def charge(request):
    # get charge
    chargeobj = models.charge.objects.all()
    return render(request,'charge.html',{
        'charge' :chargeobj
    })

def addcharge(request):
    if request.method == "GET":
        return render(request,'addcharge.html')
    elif request.method == "POST":
        print(request.POST)
        # get total objek charge
        total = models.charge.objects.all().count()
        totallen = len(str(total))
        if totallen == 1:
            idcharge = 'crg0'+str(total+1)
        else:
            idcharge = 'crg'+str(total+1)
        print(idcharge)
        namacharge = request.POST['nama']
        harga = request.POST['harga']
        # make new charge object
        new_charge = models.charge(
            idcharge=idcharge,
            jenischarge = namacharge,
            hargacharge = harga
        ).save()
        return redirect('charge')

def pelanggan(request):
    # get pelanggan object
    pelangganobj = models.pelanggan.objects.all()
    return render(request,'pelanggan.html',{
        'pelanggan':pelangganobj
    })

def updatepelanggan(request,id):
    # get selected pelanggan object
    pelangganobj = models.pelanggan.objects.get(idpelanggan =id)
    if request.method == "GET":
        tanggal = datetime.strftime(pelangganobj.tanggallahir, '%Y-%m-%d')
        return render(request,'updatepelanggan.html',{
            'pelanggan':pelangganobj,
            'tanggal' :tanggal
        })
    elif request.method == "POST":
        print(request.POST)
        nama = request.POST['nama']
        jeniskelamin = request.POST['jeniskelamin']
        tanggallahir = request.POST['tanggallahir']
        nomorhp = request.POST['number']
        pelangganobj.nama = nama
        pelangganobj.jeniskelamin = jeniskelamin
        pelangganobj.tanggallahir = tanggallahir
        pelangganobj.nomorhp = nomorhp
        pelangganobj.save()
        return redirect('pelanggan')

def deletepelanggan(request,id):
    # get selected pelanggan object
    pelangganobj = models.pelanggan.objects.get(idpelanggan = id)
    pelangganobj.delete()
    return redirect('pelanggan')

def sewa(request):
    if request.method == "GET":
        # get kamar tersedia 
        kamarobj = models.kamar.objects.filter(status = False)
        return render(request,'sewa.html',{
            'kamartersedia' : kamarobj
        })
    elif request.method == "POST":

        print(request.POST)
        # add pelanggan to database
        namapelanggan = request.POST['namapelanggan']
        jeniskelamin = request.POST['jeniskelamin']
        tanggallahir = request.POST['tanggallahir']
        nomorhp = request.POST['nomorhp']
         # get total objek charge
        total = models.pelanggan.objects.all().count()
        totallen = len(str(total))
        if totallen == 1:
            idpelanggan = 'crg0'+str(total+1)
        else:
            idpelanggan = 'crg'+str(total+1)
        print(idpelanggan)
        newpelanggan = models.pelanggan(
            idpelanggan = idpelanggan,
            nama = namapelanggan,
            jeniskelamin = jeniskelamin,
            tanggallahir = tanggallahir,
            nohp = nomorhp
        )
        newpelanggan.save()

        # Get object pelanggan
        pelangganobj = models.pelanggan.objects.get(idpelanggan = idpelanggan)
        print(pelangganobj.nama)

        # Get object kamar
        kamar = request.POST['kamar']
        kamarobj = models.kamar.objects.get(idkamar = kamar)
        
        # Get checkin data
        waktu = datetime.now()

        # Get harga kamar
        harga = 2500000

        # Update status Kamar
        kamarobj.status = True
        kamarobj.save()

        # generate id penyewaan
         # get total objek charge
        total = models.penyewaan.objects.all().count()
        totallen = len(str(total))
        if totallen == 1:
            idpenyewaan = 'crg0'+str(total+1)
        else:
            idpenyewaan = 'crg'+str(total+1)
        print(idpenyewaan)
        
        # add pemesanan to database
        new_penyewaan = models.penyewaan(
            idpenyewaan = idpenyewaan,
            idpelanggan = pelangganobj,
            idkamar = kamarobj,
            tanggalsewa = waktu,
            hargasewa = harga
        )
        new_penyewaan.save()

        # return render (request,'addtransaksi.html',{})
        return redirect('dashboard')

def cek(request):
    # get active penyewaan object
    activeobj = models.penyewaan.objects.all()
    return render(request,'cek.html',{
        'objek' : activeobj
    })

def inputcharge(request):
    return render(request,'adddetailcharge.html')