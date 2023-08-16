import numpy as np
import time

def kordinatdosyasiokuma(kordinatdosyasi): 
    """
    Bu fonksiyon, verilen metin dosyasindaki koordinatlari okur ve (x, y) çiftleri olarak bir numpy dizisi olarak geri döndürür.

    Parametreler:
        kordinatdosyasi(str): Koordinatlari içeren metin dosyasinin yolu.    
    
    Return:
        numpy dizisi: Dosyadaki (x, y) çiftleri olarak koordinat dizisi.
    """
    kordinatçiftleri = []
    with open(kordinatdosyasi, 'r') as dosya: # Dosyayi okumak icin ac
        for satir in dosya:                   # Dosyadaki her satiri oku
            x, y = satir.strip().split()     # Satirdaki x ve y koordinatlarini oku 
            kordinatçiftleri.append((float(x), float(y)))  # Koordinat çiftlerini numpy dizisine ekle
    return np.array(kordinatçiftleri)

def mesafehesaplama(birincikordinat, ikincikordinat):
    """
    İki koordinat çifti arasindaki Öklid mesafesini hesaplar.
    
    Parametreler:
        birincikordinat (tuple): 1. koordinat (x, y) çifti olarak verilir.
        ikincikordinat (tuple): 2. koordinat (x, y) çifti olarak verilir.
        
    Return:
        float: iki koordinat çifti arasindaki öklid mesafesi.
    """
    #Öklid mesafesi hesaplamak için kullanılan formül kök içinde (x1-x2)'nin karesi + (y1-y2)'nin karesi 
    return np.sqrt((birincikordinat[0] - ikincikordinat[0])**2 + (birincikordinat[1] - ikincikordinat[1])**2)

def enyakinkomşualg(kordinatçiftleri, başlangiç=0): 
    """
    En yakin komşu algoritmasini kullanarak TSP probleminin en iyi çözümünü bulmaya çalışır.
    
    parametreler:
        kordinatçiftleri (numpy array): Koordinat dizisi (x, y) çiftleri olarak verilir.
        başlangiç (int): Baslangiç olarak kullanilacak düğümün indeksi. varsayilan deger 0.
        
    Return:
        numpy array: TSP probleminin en iyi çözümünü veren şehirlerin dizisi.
    """
    şehirsayisi = kordinatçiftleri.shape[0]       # Koordinat çiftlerinin sayisini alır.
    gezilmemişşehir = list(range(şehirsayisi))    # Ziyaret edilmemis şehirlerin listesi oluşturulur.
    gezilmemişşehir.remove(başlangiç)             # Başlangıç düğümünü ziyaret edilmemis düğümlerden çıkarır.
    bulunduğuşehir = başlangiç                    # Başlangıç düğümünü geçici düğüm olarak ayarlar.
    yol = [bulunduğuşehir]                        # Başlangıç düğümünü yol dizisine ekler.
    
    while gezilmemişşehir:
        enyakinkomşualg = min(gezilmemişşehir, key=lambda x: mesafehesaplama(kordinatçiftleri[bulunduğuşehir], kordinatçiftleri[x])) # En yakın komşu algoritması
        yol.append(enyakinkomşualg)               # En yakın komşu algoritmasına göre bulunan düğümü yol dizisine ekler.
        bulunduğuşehir = enyakinkomşualg          # Bulunan düğümü geçici düğüm olarak ayarlar. 
        gezilmemişşehir.remove(bulunduğuşehir)    # Bulunan düğümü ziyaret edilmemis düğümlerden çıkarır.
        
    return np.array(yol)                          # En iyi yol dizisini döndürür.

def yoluzunluğu(kordinatçiftleri, yol):
    """
    Yolun uzunlugunu hesaplar.
    
    Parametreler:
        kordinatçiftleri (numpy array): Koordinat dizisi (x, y) çiftleri olarak verilir.
        yol (numpy array):Şehirlerin dizisi.
        
    Return:
        float: Yolun uzunlugu.
    """
    yoluzunluk = 0
    for i in range(len(yol) - 1):
        yoluzunluk += mesafehesaplama(kordinatçiftleri[yol[i]], kordinatçiftleri[yol[i + 1]])
    return  yoluzunluk

#çalışma süresini hesaplamak için kullanılan kod parçası 1
start = time.time()
# txt dosyasindaki koordinat çiftlerini oku
kordinatçiftleri = kordinatdosyasiokuma('tsp_85900_1.txt') 



#en yakın komşu algoritmasını çalıştır
optimalyol = enyakinkomşualg(kordinatçiftleri)

#print("Optiaml yol:",optimalyol)
print("Optimal yol uzunluğu:",yoluzunluğu(kordinatçiftleri, optimalyol)) 

#çalışma süresini hesaplamak için kullanılan kod parçası 2
end = time.time()
print("Toplam süre:",end - start)

"""
#çiktiyi bir metin dosyasina yazdir
with open('sonuçdosyasi.txt', 'w') as dosya:
    dosya.write("212802040, ilayda Dincbilek" + "\n")

    dosya.write("1. Sonuc: "+ str(optimalyol) + "\n") 
"""    
