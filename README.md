# 🌊 QGIS Hidrolik Hesaplayıcı

**QGIS Hidrolik Hesaplayıcı**, coğrafi veriler kullanılarak hidrolik hesaplamalar yapılmasını sağlayan bir Python uygulamasıdır. Bu proje, **QGIS** ortamında çalışarak su akışı, eğim ve debi gibi hidrolik parametrelerin hesaplanmasını kolaylaştırır.  

## 🔍 Projenin Amacı

Bu proje, **hidrolik mühendisleri, coğrafi bilgi sistemleri (GIS) uzmanları ve su yönetimi ile ilgilenen kişiler** için geliştirilmiştir. Temel amaçları şunlardır:

- **Coğrafi veriler kullanarak hidrolik hesaplamaları otomatik hale getirmek**
- **QGIS ortamında su akışı analizleri yapmak**
- **Akarsu eğimi ve debi gibi önemli parametreleri hesaplamak**
- **Manuel hesaplamaları ve hataları azaltarak mühendislik çalışmalarını hızlandırmak**

## 🚀 Kullanılan Teknolojiler

- **QGIS** → Coğrafi veri analizleri yapmak için açık kaynaklı bir CBS (Coğrafi Bilgi Sistemi) yazılımı.
- **Python** → Hidrolik hesaplamaları yapmak ve QGIS ile etkileşim sağlamak için kullanıldı.
- **PyQGIS** → QGIS'in Python API'sini kullanarak CBS verileri üzerinde işlem yapmak için.
- **GDAL** → Coğrafi verileri işleyebilmek için kullanılan güçlü bir kütüphane.
- **NumPy** → Matematiksel hesaplamaları ve veri işlemlerini kolaylaştırmak için kullanıldı.

---

## 📂 Proje Dosyaları

- **`hidrolik_hesaplayici.py`** → Ana Python betiği olup hidrolik hesaplamaları yapar.
- **`data/`** → Kullanılan örnek veri setlerini içeren klasör (eğer varsa).
- **`results/`** → Hesaplama sonuçlarını kaydetmek için kullanılan klasör.

---

## ⚙️ Hidrolik Hesaplamaların Açıklaması

Proje kapsamında yapılan işlemler şunlardır:

### 1️⃣ **Veri Yükleme ve Ön İşleme**
- Kullanıcıdan **DEM (Sayısal Yükseklik Modeli)** veya **vektör verileri (nehirler, su yolları vb.)** alınır.
- Veri **GDAL** kütüphanesi kullanılarak işlenir ve QGIS ortamına entegre edilir.
- Eksik veya hatalı veriler kontrol edilir.

### 2️⃣ **Eğim ve Akış Yönü Analizi**
- **Eğim hesaplamaları yapılır** → Su akışının yönünü ve hızı belirlemek için kullanılır.
- **Akış yönü belirlenir** → Su kütlesinin nasıl hareket ettiğini anlamak için **D8 algoritması** veya benzeri yöntemler uygulanır.

### 3️⃣ **Debi ve Akış Hızı Hesaplamaları**
- **Manning denklemi** kullanılarak kanal debisi hesaplanır:
  
  \[
  Q = \frac{1}{n} A R^{2/3} S^{1/2}
  \]

  - **Q** = Debi (m³/s)
  - **n** = Manning pürüzlülük katsayısı
  - **A** = Kesit alanı (m²)
  - **R** = Hidrolik yarıçap (m)
  - **S** = Eğim

- **Hidrolik çap ve kesit alanı hesaplanır**.

### 4️⃣ **Sonuçların Görselleştirilmesi**
- Hesaplanan akış yönleri ve debi **QGIS üzerinde görselleştirilir**.
- **Sonuçlar harita katmanları olarak eklenir** veya CSV olarak dışa aktarılır.

---

## 🔧 Kurulum ve Kullanım

### 1️⃣ **Gerekli Bağımlılıkları Yükleyin**
Aşağıdaki komutu kullanarak bağımlılıkları yükleyebilirsiniz:

```bash
pip install qgis gdal numpy
