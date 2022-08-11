from datetime import datetime
from unittest import result
from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import models

# pdfgen
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
import os

from weasyprint import HTML



# Create your views here.

def dashboard(request):
    # Kamar tersedia laki-laki
    kamartersediapa = models.kamar.objects.filter(status = False, jenis = 'laki-laki').count()
    # kamar tersedia perempuan
    kamartersediapi = models.kamar.objects.filter(status = False, jenis = "perempuan").count()
    # Total Pemesanan  
    totalpesan = models.penyewaan.objects.all().count()
    # Total charge
    totalcharge = models.charge.objects.all().count()



    return render(request,'index.html',{
        'kamartersediapa' : kamartersediapa,
        'kamarterserdiapi' : kamartersediapi,
        'totalpemesanan' : totalpesan,
        'totalcharge' : totalcharge,

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

def penyewaan(request):
    # get penyewaan object
    penyewaanobj = models.penyewaan.objects.all()
    return render(request,'penyewaan.html',{
        'penyewaan':penyewaanobj
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
    activeobj = models.kamar.objects.filter(status = "True")
    print(activeobj)
    data=[]
    
    for item in activeobj:
        selected = models.penyewaan.objects.filter(idkamar = item ).last()
        if selected:
            data.append(selected)
        else:
            continue
    print(data)
    return render(request,'cek.html',{
        'objek' : data
    })

def checkout(request,id):
    # Get selected object
    penyewaanobj = models.penyewaan.objects.get(idpenyewaan = id)

    # update status penyewaan

    # get selected kamar object
    kamarobj = models.kamar.objects.get(idkamar = penyewaanobj.idkamar.idkamar)
    print(kamarobj)
    # update status kamar

    kamarobj.status = 'False'
    kamarobj.save()
    return redirect('dashboard')

def inputcharge(request):
    data=[]
    # Get pelanggan object
    activeobj = models.kamar.objects.filter(status = "True")
    for item in activeobj:
        selected = models.penyewaan.objects.filter(idkamar = item ).last()
        if selected:
            data.append(selected)
        else:
            pass
    print(data)
    # Get Charge object
    chargeobj = models.charge.objects.all()
    if request.method == "GET":
        return render(request,'adddetailcharge.html',{
            'pelanggan':data,
            'charge' : chargeobj
        })
    elif request.method == "POST":
        print(request.POST)
        # generate id detail charge
        total = models.detailcharge.objects.all().count()
        totallen = len(str(total))
        if totallen == 1:
            idpenyewaan = 'dcr0'+str(total+1)
        else:
            idpenyewaan = 'dcr'+str(total+1)
        # Get selected charge obj
        chargeselectedobj = models.charge.objects.get(idcharge = request.POST['charge'])
        # Get selected pelanggan object
        pelangganselectedobj = models.pelanggan.objects.get(idpelanggan=request.POST['pelanggan'])

        total = int(request.POST['jumlah']) * chargeselectedobj.hargacharge
        new_detailcharge = models.detailcharge(
            iddetailcharge = idpenyewaan,
            idpelanggan = pelangganselectedobj,
            idcharge = chargeselectedobj,
            jumlahitemcharge = request.POST['jumlah'],
            hargacharge = total
        )
        new_detailcharge.save()
        return redirect('dashboard')

def detailcharge(request,id):
    # Get selected detailcharge
    print(id)
    detailchargeobj = models.detailcharge.objects.filter(idpelanggan = id)
    return render(request,'detailcharge.html',{
        'detailcharge':detailchargeobj
    })

def laporan(request):
    if request.method == "GET":
        return render(request,'laporan.html')
    elif request.method == "POST":
        detailobj =[]
        # Get selected penyewaan object
        mulai = request.POST['mulai']
        akhir = request.POST['akhir']
        penyewaanobj = models.penyewaan.objects.filter(tanggalsewa__range=(mulai,akhir))
        for item in penyewaanobj:
            data=[]
            # Get selected detailcharge by idpelanggan
            detailchargeobj = models.detailcharge.objects.filter(idpelanggan = item.idpelanggan)
            data.append(item)
            data.append(detailchargeobj)
            totalcharge=detailchargeobj.aggregate(Sum('hargacharge'))
            biayasewa = item.hargasewa
            if totalcharge['hargacharge__sum'] == None:
                total = biayasewa
            else:
                total = totalcharge['hargacharge__sum']+biayasewa
            data.append(total)
            detailobj.append(data)
            total += total
    
        pemasukan = []
        for harga in detailobj:
            pemasukan.append(harga[2])
        totalpemasukan = sum(pemasukan)

        return render(request,'detaillaporan.html',{
            'detailobjek' :detailobj,
            'tanggalmulai' : mulai,
            'tanggalakhir' : akhir,
            'pemasukan' : totalpemasukan

        })

def laporanpdf(request,mulai,akhir):

    detailobj =[]
    # Get selected penyewaan object
    penyewaanobj = models.penyewaan.objects.filter(tanggalsewa__range=(mulai,akhir))
    for item in penyewaanobj:
        data=[]
        # Get selected detailcharge by idpelanggan
        detailchargeobj = models.detailcharge.objects.filter(idpelanggan = item.idpelanggan)
        data.append(item)
        data.append(detailchargeobj)
        totalcharge=detailchargeobj.aggregate(Sum('hargacharge'))
        biayasewa = item.hargasewa
        print(totalcharge)
        if totalcharge['hargacharge__sum'] == None:
            total = biayasewa
        else:
            total = totalcharge['hargacharge__sum']+biayasewa
        data.append(total)
        detailobj.append(data)
    
    pemasukan = []
    for harga in detailobj:
        pemasukan.append(harga[2])
    totalpemasukan = sum(pemasukan)

    totaltransaksi = penyewaanobj.count()
    
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'laporanpdf.html',{
            'detailobjek' : detailobj,
            'pemasukan' : totalpemasukan,
            'totaltransaksi' : totaltransaksi,
            'mulai' :mulai,
            'akhir' : akhir
            })
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    render(request,'laporanpdf.html')
    
    return response

def notapdf(request,id):
    # Get selected object 
    pelangganobj = models.pelanggan.objects.get(idpelanggan = id)
    # Get Detail penyewaan
    penyewaanobj = models.penyewaan.objects.get(idpelanggan = id)
    # Get detail charge
    detailchargeobj = models.detailcharge.objects.filter(idpelanggan = id)
    # total charge
    totalcharge = detailchargeobj.aggregate(Sum('hargacharge'))
    totalcharge = totalcharge['hargacharge__sum']
    if totalcharge is not None : 
        grandtotal = int(totalcharge)+int(penyewaanobj.hargasewa)
    else :
        grandtotal = int(penyewaanobj.hargasewa)
    
    print(pelangganobj)
    print(penyewaanobj)
    print(detailchargeobj)
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'notapdf.html',{
            'pelanggan' : pelangganobj,
            'penyewaan' : penyewaanobj,
            'detailcharge' : detailchargeobj,
            'totalcharge' : totalcharge,
            'grandtotal' : grandtotal
            
            }
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    return response
def pdfgen(request):

    # GET pelanggan
    pelangganobj = models.pelanggan.objects.all()

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_of_students.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string(
        'pelanggan.html',{'pelanggan' : pelangganobj, 'total':0}
    )
    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    return response