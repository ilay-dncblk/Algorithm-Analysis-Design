import numpy as np
import random
import math
import xlsxwriter

dosyalar = ['wl_16_1.txt', 'wl_200_2.txt', 'wl_500_3.txt']

workbook = xlsxwriter.Workbook("veri.xlsx")
worksheet = workbook.add_worksheet()

def veriOkuma(dosya_adi):
    with open(dosya_adi, 'r') as f:
        veri = f.read()
    return veri

def veri_çevirme(veri):
    satir = veri.split('\n')
    depolar, müşteriSayisi = map(int, satir[0].split())

    depoKapasiteleri = []
    depoMaliyetleri = []
    for i in range(1, depolar + 1):
        depoKapasitesi, depoMaliyeti = map(float, satir[i].split())
        depoKapasiteleri.append(depoKapasitesi)
        depoMaliyetleri.append(depoMaliyeti)

    müşteriTalepleri = []
    müşteriMaliyetleri = []
    for i in range(depolar + 1, len(satir), 2):
        müşteriTalebi = float(satir[i])
        müşteriMaliyeti = list(map(float, satir[i + 1].split()))
        müşteriTalepleri.append(müşteriTalebi)
        müşteriMaliyetleri.append(müşteriMaliyeti)
    
    return depolar, müşteriSayisi, depoKapasiteleri, depoMaliyetleri, müşteriTalepleri, müşteriMaliyetleri

def rastgeleKomşu(bireysel, depolar, müşteriSayisi):
    # Rastgele bir müşteriyi rastgele bir depoya taşıyarak rastgele bir komşu oluşturun
    komşu = bireysel.copy()
    müşteriNumarasi = random.randint(0, müşteriSayisi - 1)
    depoNumarasi = random.randint(0, depolar - 1)
    komşu[müşteriNumarasi] = depoNumarasi
    return komşu

def uygunluguDeğerlendirme(bireysel, depoMaliyetleri, müşteriMaliyetleri, depoKapasiteleri, müşteriTalepleri, depolar):
    # Negatif maliyeti maksimize ederiz (maliyeti minimize ederiz) ancak negatif maliyete sahip olamayız

    # Çözümün toplam maliyetini hesaplayın
    toplamMaliyet = 0
    kullanilanDepolar = set()
    for müşteri, depo in enumerate(bireysel):
        toplamMaliyet += müşteriMaliyetleri[müşteri][depo]
        kullanilanDepolar.add(depo)
    for depo in kullanilanDepolar:
        toplamMaliyet += depoMaliyetleri[depo]
        
    # Çözüm tarafından kullanılan toplam alanı hesaplayın
    totalAlan = np.zeros(depolar)
    for müşteri, depo in enumerate(bireysel):
        totalAlan[depo] += müşteriTalepleri[müşteri]
        
    # Mevcut olandan daha fazla alan kullanıyorsa çözümü cezalandırın
    for depo in range(depolar):
        if totalAlan[depo] > depoKapasiteleri[depo]:
            toplamMaliyet += 1000 * (totalAlan[depo] - depoKapasiteleri[depo])
            
    return -toplamMaliyet

def bireyselİşleme(depolar, müşteriSayisi):
    return [random.randint(0, depolar - 1) for _ in range(müşteriSayisi)]

def ihtimalDeğerlendirme(sonUygunluk, yeniUygunluk, sicaklik):
    # Uygunluk değerlerindeki farka ve sıcaklığa dayalı olarak kabul olasılığını hesaplayın
    if yeniUygunluk > sonUygunluk:
        return 1.0
    else:
        return math.exp((yeniUygunluk - sonUygunluk) / sicaklik)

def benzetimliTavlamaAlg(depolar, müşteriSayisi, depoMaliyetleri, müşteriMaliyetleri, depoKapasiteleri, müşteriTalepleri,
                        ilkBirey, ilkSicaklik, soğutmaOrani, maxYineleme):
    mevcutBirey = ilkBirey
    eniyiBirey = mevcutBirey
    sonUygunluk = uygunluguDeğerlendirme(mevcutBirey, depoMaliyetleri, müşteriMaliyetleri, depoKapasiteleri, müşteriTalepleri, depolar)
    enUyumlu = sonUygunluk
    sicaklik = ilkSicaklik

    for iteration in range(maxYineleme):
        # Rastgele bir komşu oluşturun
        komşu = rastgeleKomşu(mevcutBirey, depolar, müşteriSayisi)
        yeniUygunluk = uygunluguDeğerlendirme(komşu, depoMaliyetleri, müşteriMaliyetleri, depoKapasiteleri, müşteriTalepleri, depolar)

        # Komşunun mevcut çözüm olarak kabul edilip edilmeyeceğini belirleyin
        if ihtimalDeğerlendirme(sonUygunluk, yeniUygunluk, sicaklik) > random.random():
            mevcutBirey = komşu
            sonUygunluk = yeniUygunluk

        # Gerekirse en iyi çözümü güncelleme
        if yeniUygunluk > enUyumlu:
            eniyiBirey = komşu
            enUyumlu = yeniUygunluk

        sicaklik *= soğutmaOrani

    return -enUyumlu, eniyiBirey

def benzetimliTavlamaÇaliştir(veri_dosyasi, ilkSicaklik, soğutmaOrani, maxYineleme, dosyaSayisi):
    veri = veriOkuma(veri_dosyasi)
    depolar, müşteriSayisi, depoKapasiteleri, depoMaliyetleri, müşteriTalepleri, müşteriMaliyetleri = veri_çevirme(veri)
    
    # Mutlak en iyi çözüm için değişkenleri başlatın
    mutlakEnUyumlu = math.inf
    mutlakEniyiBirey = None
    
    # Algoritmayı 10 kez çalıştırın ve en düşük maliyetli ve en iyi çözümü yazdırın
    for i in range(10):
        ilkBirey = bireyselİşleme(depolar, müşteriSayisi)
        uygunluk, bireysel = benzetimliTavlamaAlg(depolar, müşteriSayisi, depoMaliyetleri, müşteriMaliyetleri,
                                                 depoKapasiteleri, müşteriTalepleri, ilkBirey,
                                                 ilkSicaklik, soğutmaOrani, maxYineleme)
        if uygunluk < mutlakEnUyumlu:
            mutlakEnUyumlu = uygunluk
            mutlakEniyiBirey = bireysel
    
    print(f'En iyi Çözüm: {mutlakEniyiBirey}')
    print(f'En iyi Yerleştirme: {mutlakEnUyumlu}')

    # Sonuçları bir Excel dosyasına yazma
    def xlsxYazdirma(dosyaSayisi):
        eniyiBireydizisi= str(mutlakEniyiBirey)
        eniyiBireydizisi= eniyiBireydizisi.replace('[', '')
        eniyiBireydizisi= eniyiBireydizisi.replace(']', '')
        eniyiBireydizisi= eniyiBireydizisi.replace(',', '')
        
        worksheet.write(2+dosyaSayisi, 0, depolar)
        worksheet.write(2+dosyaSayisi, 1, mutlakEnUyumlu)
        worksheet.write(2+dosyaSayisi, 2, eniyiBireydizisi)

    xlsxYazdirma(dosyaSayisi)

def dosyayaYaz():
    worksheet.write(0, 0, '212802040 İlayda DİNÇBİLEK')
    worksheet.write(1, 0, 'Dosya Boyutu')
    worksheet.write(1, 1, 'Optimal Maliyet')
    worksheet.write(1, 2, 'Müşteriye Atanan Depolar')

for i in range(len(dosyalar)):
    print(f'Dosya: {dosyalar[i]}')
    benzetimliTavlamaÇaliştir(dosyalar[i], 1000, 0.999, 10000,i)
    print("--------------------------------------------------")
    dosyayaYaz()
    
workbook.close()