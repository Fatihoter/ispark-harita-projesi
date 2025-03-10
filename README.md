# İstanbul İSPARK Harita Uygulaması

İstanbul'daki İSPARK otoparklarını interaktif bir harita üzerinde görüntüleyen, filtreleme yapabilen ve kullanıcıya en yakın otoparka rota çizen web uygulaması.

## 🚀 Özellikler

- **İSPARK Otoparkları Görüntüleme:** Tüm İSPARK noktalarını harita üzerinde görün
- **Konum Bazlı Özellikler:** Kullanıcının konumunu tespit ederek en yakın otoparkı bulma
- **Akıllı Filtreleme:** İlçe ve otopark adına göre filtreleme
- **Rota Çizimi:** Kullanıcının konumundan seçilen otoparka OSRM kullanarak detaylı yol tarifi
- **Detaylı Bilgi:** Her otopark için kapasite, doluluk oranı, çalışma saatleri gibi detaylar
- **Zoom Seviyesine Göre Marker Gruplandırma:** Farklı yakınlaştırma seviyelerinde dinamik görünüm

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python, Flask, SQLAlchemy, GeoAlchemy2
- **Veritabanı:** PostgreSQL, PostGIS (Coğrafi veri desteği)
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Harita:** Leaflet.js, Turf.js, Leaflet Routing Machine, OSRM
- **API Entegrasyonu:** İBB İSPARK API

## 📸 Uygulama Ekran Görüntüleri

![Ana Ekran](screenshots/Ana_Ekran.png)
![Ana Harita Ekranı](screenshots/Ana_Harita_Ekranı.png)
![İlçe Bazlı Harita Filtreleme](screenshots/İlçe_Bazlı_Harita_Filtreleme.png)
![Otopark Listeleme ve Sorgulama](screenshots/Otopark_Listeleme_ve_Sorgulama.png)
![Otoparka Rota](screenshots/Otoparka_Rota.png)
![Otoparka Rota-2](screenshots/Otoparka_Rota-2.png)

## 🌐 Veri Kaynağı

Otopark konumları veritabanında önceden kayıtlıdır. Doluluk oranları ve güncel bilgiler [İstanbul Büyükşehir Belediyesi (İBB) API'sinden](https://api.ibb.gov.tr/ispark/Park) gerçek zamanlı olarak alınmaktadır.

- **Statik Veriler:** Otopark konumları ve temel bilgiler veritabanında depolanmış
- **Dinamik Veriler:** Anlık doluluk oranları İBB API'sinden çekilmektedir
- **API Endpoint:** `https://api.ibb.gov.tr/ispark/Park`

## 💻 Kurulum

1. Repo'yu klonlayın:
   ```bash
   git clone https://github.com/Fatihoter/ispark-harita-projesi
   cd ispark-harita-projesi