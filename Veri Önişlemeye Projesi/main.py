from tkinter import *
import matplotlib.pyplot as plt
import math
import random

eksikVeriSayisi = 400

""" Nitelikler : 
13 Nitelik  517 Örnek 
X     - Belirli bil bölgedeki haritanın x ekseni
Y     - Belirli bil bölgedeki haritanın y ekseni
MONTH - Ay
DAY   - Gün
FFMC  - Orman çöpü yakıtlarının nemi
DMC   - Ayrışmış organik malzemenin nemini temsil eder. 
DC    - Toprağın derinliklerinde kurumayı temsil eder
ISI   - Yangın yoğunluğunun sayısal bir derecesidir.
TEMP  - Santigrat derece cinsinden sıcaklık
RH    - Bağıl nem 
WIND  - Rüzgar hızı 
RAIN  - Yağmur miktarı 
AREA  - Yanmış orman alanı
"""



liste_Nitelikler = []
Listem = []
yedekListe = []
sozluk = dict()
orta = (len(Listem)+1)/2

eksikVeriTamamlamaYontemleri = ["Ortalama ile tamamla","Medyan ile tamamla","Mod ile tamamla"]
islemListesi = ["Ortalama","Medyan","Mod","Frekans", "IQR","Aykırı Değerler","Beş Sayı Özeti", "Kutu Grafiği", "Varyans -- Standart sapma"]

nitelikKontrol = 0
with open("ugur.txt", "r+") as Dosya:
    ind = 0
    Veriler = Dosya.readlines()
    for satir in Veriler:
        if satir != "":
            sutun = satir.split(",")
            if nitelikKontrol != 0:
                Listem.append(list())
                for sayac in range(len(sutun)):
                    if sayac != (len(sutun)-1):
                        Listem[ind].append(sutun[sayac])
                    else:
                        Listem[ind].append(sutun[sayac][0:-1])
                ind = ind + 1
            else :
                for sayac in range(len(sutun)):
                    if sayac != (len(sutun)-1):
                        liste_Nitelikler.append(sutun[sayac])
                    else:
                        liste_Nitelikler.append(sutun[sayac][0:-1])
        nitelikKontrol = nitelikKontrol + 1
i = 0




## Eksik veri ekleme
for i in range(eksikVeriSayisi):
    satir = random.randint(0,len(Listem)-1)
    sutun = random.randint(0,len(liste_Nitelikler)-1)

    if Listem[satir][sutun] != "?":
        Listem[satir][sutun] = "?"
    else:
        while True:
            satir = random.randint(0, len(Listem) - 1)
            sutun = random.randint(0, len(liste_Nitelikler) - 1)
            if Listem[satir][sutun] != "?":
                Listem[satir][sutun] = "?"
                break





##Listeyi baska bir listeye atama.
def yedekListeOlustur():
    geciciListem = []
    for i in range(len(Listem)):
        geciciListem.append(list())
        for j in range(len(Listem[i])):
            geciciListem[i].append(Listem[i][j])
    return geciciListem

yedekListe = yedekListeOlustur()

def ortalamaBul():
    metin_alani.delete("1.0", "end")
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END,"Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for i in range(len(liste_Nitelikler)):
            toplam = 0
            index = 0
            for A in yedekListe:
                toplam = toplam + float(A[i])
                index = index + 1
            Ortalama = toplam / index
            Ortalama = round(Ortalama, 2)
            metin_alani.insert(END, "'  {}  '\nOrtalama: {}\nVeri Sayisi :{}\nToplam:{}\n------------\n".format(liste_Nitelikler[i],Ortalama,index, toplam),'style' )

def medyanBul():
    siralanacakListe = []
    metin_alani.delete("1.0", "end")
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for i in range(len(liste_Nitelikler)):
            siralanacakListe.clear()
            for B in yedekListe:
                    siralanacakListe.append(B[i])
            if len(siralanacakListe) != 0:
                for x in range(0, len(siralanacakListe)):
                    for y in range(0, len(siralanacakListe) - 1):
                        if float(siralanacakListe[y]) > float(siralanacakListe[y + 1]):
                            siralanacakListe[y], siralanacakListe[y + 1] = siralanacakListe[y + 1], siralanacakListe[y]
            medyanIndexi = int(((len(siralanacakListe) + 1) / 2) - 1)
            medyan = siralanacakListe[medyanIndexi]
            metin_alani.insert(END, "{}\nMedyan: {}\n------------\n".format(liste_Nitelikler[i], medyan ),'style')

def modBul():
    sozluk.clear()
    nitelik = nitelikSecimi.get()
    metin_alani.delete("1.0", "end")
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for i in range(len(liste_Nitelikler)):
            for B in yedekListe:
                if (B[i]) in sozluk:
                    sozluk[B[i]] = sozluk[B[i]] + 1
                else:
                    sozluk[B[i]] = 1
            enbuyukkey = 0
            enbuyukvalue = 0
            for key in sozluk:
                if sozluk[key] > enbuyukvalue:
                    enbuyukkey = key
                    enbuyukvalue = sozluk[key]
            metin_alani.insert(END, "{}\nMod: {}\nTekrar Sayisi: {}\n------\n".format(liste_Nitelikler[i], enbuyukkey,enbuyukvalue),'style')
            sozluk.clear()

def frekansBul():
    nitelik = nitelikSecimi.get()
    if nitelik != "Nitelik Seçiniz" and nitelik != "Hepsi":
        nitelikNo = 0
        for i in liste_Nitelikler:
            if i != nitelik:
                nitelikNo = nitelikNo + 1
            else:
                break
    else:
        metin_alani.delete("1.0", "end")
        metin_alani.insert(END, "Yanlış nitelik seçimi",'style')
        return

    FrekansVeri=dict()
    FrekansVeri.clear()
    for A in yedekListe:
        if A[nitelikNo] in FrekansVeri:
            FrekansVeri[A[nitelikNo]] += 1
        else:
            FrekansVeri[A[nitelikNo]] = 1
    FrekansListemX = []
    FrekansListemY = []
    for i, j in FrekansVeri.items():
        FrekansListemX.append(float(i))
        FrekansListemY.append(j)
    enbuyuk=0
    for i in FrekansListemX:
        if i > enbuyuk:
            enbuyuk = i
    plt.xlim(0,enbuyuk+1)
    plt.bar(FrekansListemX, FrekansListemY,width=0.1, color=['red', 'grey'])
    plt.xlabel('Deger')
    plt.ylabel('Tekrar')
    plt.title('FREKANS')
    plt.show()

def iqrBul():
    metin_alani.delete("1.0", "end")
    siralanacakListe = []
    ## Nitelik Değeri Bulma
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for listeIndexi in range(len(liste_Nitelikler)):
            siralanacakListe.clear()
            ##Listenin Siralanmasi
            for B in yedekListe:
                siralanacakListe.append(B[listeIndexi])
            for i in range(0, len(siralanacakListe)):
                for j in range(0, len(siralanacakListe) - 1):
                    if float(siralanacakListe[j]) > float(siralanacakListe[j + 1]):
                        siralanacakListe[j], siralanacakListe[j + 1] = siralanacakListe[j + 1], siralanacakListe[j]
            ilkCeyrek = (((len(yedekListe) + 1) / 4) - 1)
            ucuncuCeyrek = ilkCeyrek * 3
            tamSayimiKontrolu = ilkCeyrek - int(ilkCeyrek)
            if (tamSayimiKontrolu != 0):
                ilkCeyrekDegeri = (float(siralanacakListe[int(ilkCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ilkCeyrek)])) / 2
                ucuncuCeyrekDegeri = (float(siralanacakListe[int(ucuncuCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ucuncuCeyrek)])) / 2
            else:
                ilkCeyrekDegeri = float(siralanacakListe[int(ilkCeyrek)])
                ucuncuCeyrekDegeri = float(siralanacakListe[int(ucuncuCeyrek)])
            iqrDegeri = ucuncuCeyrekDegeri - ilkCeyrekDegeri
            metin_alani.insert(END, "{}\nIQR: {}\nİlk Çeyrek değeri: {}\nÜçüncü Çeyrek değeri: {}\n-------\n"
                               .format(liste_Nitelikler[listeIndexi],iqrDegeri,ilkCeyrekDegeri,ucuncuCeyrekDegeri),'style')

def ayrikDegerBul():
    siralanacakListe = []
    listeAykiriDegerler = []
    metin_alani.delete("1.0", "end")
    ## Nitelik Değeri Bulma
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for listeIndexi in range(len(liste_Nitelikler)):
            siralanacakListe.clear()
            for B in yedekListe:
                siralanacakListe.append(B[listeIndexi])
            for i in range(0, len(siralanacakListe)):
                for j in range(0, len(siralanacakListe) - 1):
                    if float(siralanacakListe[j]) > float(siralanacakListe[j + 1]):
                        siralanacakListe[j], siralanacakListe[j + 1] = siralanacakListe[j + 1], siralanacakListe[j]
            ## Çeyrekleri ve Değerlerini Bulma
            ilkCeyrek = (((len(yedekListe) + 1) / 4) - 1)
            ucuncuCeyrek = ilkCeyrek * 3
            tamSayimiKontrolu = ilkCeyrek - int(ilkCeyrek)
            if (tamSayimiKontrolu != 0):
                ilkCeyrekDegeri = (float(siralanacakListe[int(ilkCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ilkCeyrek)])) / 2
                ucuncuCeyrekDegeri = (float(siralanacakListe[int(ucuncuCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ucuncuCeyrek)])) / 2
            else:
                ilkCeyrekDegeri = float(siralanacakListe[int(ilkCeyrek)])
                ucuncuCeyrekDegeri = float(siralanacakListe[int(ucuncuCeyrek)])
            iqrDegeri = ucuncuCeyrekDegeri - ilkCeyrekDegeri
            altSinir = ilkCeyrekDegeri - (1.5 * iqrDegeri)
            ustSinir = ucuncuCeyrekDegeri + (1.5 * iqrDegeri)
            listeAykiriDegerler.clear()
            for i in siralanacakListe:
                if float(i) < altSinir:
                    listeAykiriDegerler.append(float(i))
                elif float(i) > ustSinir:
                    listeAykiriDegerler.append(float(i))
            metin_alani.insert(END,
                               "{}\nAlt Sınır: {}\nUst Sınır: {}\nAykiri Değerlerin Listesi {}\n-----\n"
                               .format(liste_Nitelikler[listeIndexi], altSinir, ustSinir, listeAykiriDegerler),'style')

def besSayiOzeti():
    metin_alani.delete("1.0", "end")
    ## Nitelik Değeri Bulma
    siralanacakListe = []
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for listeIndexi in range(len(liste_Nitelikler)):
            siralanacakListe.clear()
            for B in yedekListe:
                siralanacakListe.append(B[listeIndexi])
            for i in range(0, len(siralanacakListe)):
                for j in range(0, len(siralanacakListe) - 1):
                    if float(siralanacakListe[j]) > float(siralanacakListe[j + 1]):
                        siralanacakListe[j], siralanacakListe[j + 1] = siralanacakListe[j + 1], siralanacakListe[j]
            ilkCeyrek = (((len(yedekListe) + 1) / 4) - 1)
            ucuncuCeyrek = ilkCeyrek * 3
            tamSayimiKontrolu = ilkCeyrek - int(ilkCeyrek)
            if (tamSayimiKontrolu != 0):
                ilkCeyrekDegeri = (float(siralanacakListe[int(ilkCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ilkCeyrek)])) / 2
                ucuncuCeyrekDegeri = (float(siralanacakListe[int(ucuncuCeyrek + 0.5)]) + float(
                    siralanacakListe[int(ucuncuCeyrek)])) / 2
            else:
                ilkCeyrekDegeri = float(siralanacakListe[int(ilkCeyrek)])
                ucuncuCeyrekDegeri = float(siralanacakListe[int(ucuncuCeyrek)])
            ## MEDYAN BUL
            ortanca = (((len(yedekListe) + 1) / 2) - 1)
            tamSayimiKontrolu = ortanca - int(ortanca)
            if (tamSayimiKontrolu != 0):
                ortancaDegeri = (float(siralanacakListe[int(ortanca + 0.5)]) + float(
                    siralanacakListe[int(ortanca)])) / 2
            else:
                ortancaDegeri = float(siralanacakListe[int(ortanca)])
            iqrDegeri = ucuncuCeyrekDegeri - ilkCeyrekDegeri
            metin_alani.insert(END,
                               "{}\nMinimum: {}\nQ1: {}\nMedyan: {}\nQ3: {}\nMaximum: {}\n-----\n"
                               .format(liste_Nitelikler[listeIndexi],siralanacakListe[0], ilkCeyrekDegeri, ortancaDegeri, ucuncuCeyrekDegeri,
                                       siralanacakListe[len(siralanacakListe) - 1]),'style')

def kutuGrafigiCizdir():
    ## Nitelik Değeri Bulma
    nitelik = nitelikSecimi.get()
    if nitelik != "Nitelik Seçiniz" and nitelik != "Hepsi":
        nitelikNo = 0
        for i in liste_Nitelikler:
            if i != nitelik:
                nitelikNo = nitelikNo + 1
            else:
                break
    else:
        metin_alani.delete("1.0", "end")
        metin_alani.insert(END, "Yanlış nitelik seçimi",'style')
        return

    ## Değerleri Sıralama
    siralanacakListe = []
    for B in yedekListe:
        siralanacakListe.append(B[nitelikNo])
    for i in range(0, len(siralanacakListe)):
        for j in range(0, len(siralanacakListe) - 1):
            if float(siralanacakListe[j]) > float(siralanacakListe[j + 1]):
                siralanacakListe[j], siralanacakListe[j + 1] = siralanacakListe[j + 1], siralanacakListe[j]
    listeFloat = []
    for i in siralanacakListe:
        degerler = round(float(i), 2)
        listeFloat.append(degerler)

    plt.boxplot(listeFloat)
    plt.show()

def varyanstandartsapmaBul():
    metin_alani.delete("1.0", "end")
    nitelik = nitelikSecimi.get()
    if nitelik != "Hepsi":
        metin_alani.insert(END, "Nitelik seçimi doğru değil. -> Hepsi <-",'style')
    if nitelik == "Hepsi":
        for listeIndexi in range(len(liste_Nitelikler)):
            toplam = 0
            index = 0
            for A in yedekListe:
                toplam = toplam + float(A[listeIndexi])
                index = index + 1
            ortalama = toplam / index
            x = 0
            for i in yedekListe:
                x += ((float(i[listeIndexi]) - ortalama) ** 2)
            varyans = x / (len(yedekListe) - 1)
            standartSapma = math.sqrt(varyans)
            metin_alani.insert(END,
                               "{}\nVaryasn: {}\nStandart sapma: {}\n-----\n"
                               .format(liste_Nitelikler[listeIndexi],varyans, standartSapma),'style')

def islemler():
    eksikVeriSay = 0
    for i in yedekListe:
        for j in i:
            if j == "?":
                eksikVeriSay += 1
    if eksikVeriSay != 0:
        metin_alani.delete("1.0", "end")
        metin_alani.insert(END, "Veri Setinde Eksik Veri Bulunmaktadır.",'style')
        return
    islem = islemSecimi.get()
    nitelik = nitelikSecimi.get()
    if (islem != "Islemi Seciniz"):
        if islem == "Ortalama":
            ortalamaBul()
        elif islem == "Medyan":
            medyanBul()
        elif islem == "Mod":
            modBul()
        elif islem == "Frekans":
            frekansBul()
        elif islem == "IQR":
            iqrBul()
        elif islem == "Aykırı Değerler":
            ayrikDegerBul()
        elif islem == "Beş Sayı Özeti":
            besSayiOzeti()
        elif islem == "Kutu Grafiği":
            kutuGrafigiCizdir()
        elif islem == "Varyans -- Standart sapma":
            varyanstandartsapmaBul()

def verileriYazdir():
    metin_alani.delete("1.0", "end")
    metin_alani.insert(END, liste_Nitelikler,'style')
    metin_alani.insert(END, '\n','style')
    for x in yedekListe:
        metin_alani.insert(END, x,'style')
        metin_alani.insert(END, '\n','style')

def eksikVerileriTamamla():
    global yedekListe
    if veriTamamlamaSecimi.get() == "Ortalama ile tamamla":
        yedekListe = yedekListeOlustur()
        deneme = 0
        for i in range(len(liste_Nitelikler)):
            toplam = 0
            index = 0
            for A in yedekListe:
                if A[i] != "?":
                    toplam = toplam + float(A[i])
                    index = index + 1
            Ortalama = toplam / index
            Ortalama = round(Ortalama, 2)

            for A in yedekListe:
                if A[i] == "?":
                    A[i] = str(Ortalama)
                    deneme = deneme + 1
    elif veriTamamlamaSecimi.get() == "Medyan ile tamamla":
        siralanacakListe = []
        yedekListe = yedekListeOlustur()
        deneme = 0
        for i in range(len(liste_Nitelikler)):
            siralanacakListe.clear()
            for B in yedekListe:
                if B[i] != "?":
                    siralanacakListe.append(B[i])
            if len(siralanacakListe) != 0:
                for x in range(0, len(siralanacakListe)):
                    for y in range(0, len(siralanacakListe) - 1):
                        if float(siralanacakListe[y]) > float(siralanacakListe[y + 1]):
                            siralanacakListe[y], siralanacakListe[y + 1] = siralanacakListe[y + 1], siralanacakListe[y]
                orta = int(((len(siralanacakListe) + 1) / 2) - 1)
                for s in yedekListe:
                    if s[i] == "?":
                        s[i] = str(siralanacakListe[orta])
                        deneme = deneme + 1
    elif veriTamamlamaSecimi.get() == "Mod ile tamamla":
        yedekListe = yedekListeOlustur()
        for i in range(len(liste_Nitelikler)):
            sozluk.clear()
            for B in yedekListe:
                if B[i] != "?":
                    if (B[i]) in sozluk:
                        sozluk[B[i]] = sozluk[B[i]] + 1
                    else:
                        sozluk[B[i]] = 1
            enbuyukkey = 0
            enbuyukvalue = 0
            for key in sozluk:
                if sozluk[key] > enbuyukvalue:
                    enbuyukkey = key
                    enbuyukvalue = sozluk[key]
            for s in yedekListe:
                if s[i] == "?":
                    s[i] = str(enbuyukkey)
    else:
        metin_alani.delete("1.0", "end")
        metin_alani.insert(END, "Eksik veri tamamlama yöntemini seçiniz",'style')

master = Tk()
master.title("Veri Onislemeye Giris")

## ALANLAR
canvas = Canvas(master, heigh=750, width=670)
canvas.pack()
frame_Tum = Frame(master, bg = "#C0C0C0")
frame_Tum.place(relwidth=1,relheight=1)
frame_Ust = Frame(frame_Tum, bg="light cyan")
frame_Ust.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.06)
frame_AraRenk4 = Frame(frame_Tum, bg="#000000")
frame_AraRenk4.place(relx=0.01, rely=0.074, relwidth=0.98, relheight=0.005)
frame_VeriSetiniYazdir = Frame(frame_Tum, bg="#607D8B")
frame_VeriSetiniYazdir.place(relx=0.01, rely=0.084, relwidth=0.98, relheight=0.04)
frame_AraRenk2 = Frame(frame_Tum, bg="#000000")
frame_AraRenk2.place(relx=0.01, rely=0.128, relwidth=0.98, relheight=0.005)
frame_EksikVeriTamamlamaMenu = Frame(frame_Tum,bg="#607D8B")
frame_EksikVeriTamamlamaMenu.place(relx=0.01, rely=0.137, relwidth=0.485, relheight=0.04)
frame_EksikVeriTamamlamaButonu = Frame(frame_Tum, bg="#607D8B")
frame_EksikVeriTamamlamaButonu.place(relx=0.505, rely=0.137, relwidth=0.485, relheight=0.04)
frame_AraRenk1 = Frame(frame_Tum, bg="#000000")
frame_AraRenk1.place(relx=0.01, rely=0.181, relwidth=0.98, relheight=0.005)
frame_AltSol = Frame(frame_Tum, bg="#607D8B")
frame_AltSol.place(relx=0.01, rely=0.190, relwidth=0.485, relheight=0.04)
frame_AltSag = Frame(frame_Tum, bg="#607D8B")
frame_AltSag.place(relx=0.01, rely=0.233, relwidth=0.485, relheight=0.04)
frame_Buton = Frame(frame_Tum,bg="#607D8B")
frame_Buton.place(relx=0.505, rely=0.190, relwidth=0.485, relheight=0.083)
frame_AraRenk3 = Frame(frame_Tum, bg="#000000")
frame_AraRenk3.place(relx=0.01, rely=0.277, relwidth=0.98, relheight=0.005)
frame_MetinAlani = Frame(frame_Tum,bg="#607D8B")
frame_MetinAlani.place(relx=0.01, rely=0.286, relwidth=0.98, relheight=0.694)

lbl_Ust = Label(frame_Ust, text="Veri Onislemeye Giris", bg="light cyan", font="Courier 20 bold").pack(padx=10,pady=10)

veriTamamlamaSecimi = StringVar(frame_EksikVeriTamamlamaMenu)
veriTamamlamaSecimi.set("Veri tamamlama yöntemini seçiniz.")  ##Default değer atadik.
veriTamamlamaSecimiMenu = OptionMenu(frame_EksikVeriTamamlamaMenu, veriTamamlamaSecimi ,*eksikVeriTamamlamaYontemleri)
veriTamamlamaSecimiMenu.config(width=100, height=100,font="Courier 10")
veriTamamlamaSecimiMenu.pack()

nitelikSecimi = StringVar(frame_AltSag)
nitelikSecimi.set("Nitelik Seçiniz")  ##Default değer atadik.
nitelikSevimiMenu = OptionMenu(frame_AltSag,nitelikSecimi,"Hepsi",*liste_Nitelikler)
nitelikSevimiMenu.config(width=100, height=100,font="Courier 12")
nitelikSevimiMenu.pack()

islemSecimi = StringVar(frame_AltSol)
islemSecimi.set("İslem Seçiniz")  ##Default değer atadik.
islemSecimiMenu = OptionMenu(frame_AltSol,islemSecimi,*islemListesi)
islemSecimiMenu.config(width=100, height=100,font="Courier 12")
islemSecimiMenu.pack()

islemSecButonu = Button(frame_Buton, text='Hesapla', command=islemler,font="Courier 12",width=100,height=100)
islemSecButonu.pack()

verileriYazButonu = Button(frame_VeriSetiniYazdir, text='Verileri Goster', command=verileriYazdir,width=100,height=100,font="Courier 15")
verileriYazButonu.pack()

eksikVerileriTamamlamaButonu = Button(frame_EksikVeriTamamlamaButonu, text='Eksik Verileri Tamamla',command=eksikVerileriTamamla,width=100,height=100,font="Courier 12")
eksikVerileriTamamlamaButonu.pack()

metin_alani = Text(frame_MetinAlani, height=100, width=100, bg="light cyan")
metin_alani.tag_configure('style', font=("Courier", 14))
metin_alani.pack(padx=1, pady=1)

master.mainloop()  ## Mainloop yazmazsak arayüz görükür ve tekrar kapanır
