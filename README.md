## Blockchain Absen Anti Titip Absen
Proyek ini merupakan implementasi sistem desentralisasi berbasis Blockchain untuk mengatasi permasalahan *Titip Absen* di lingkungan akademik. Dengan menggabungkan teknologi Distributed Ledger dan Digital Signature, kami memastikan setiap data kehadiran bersifat *aman, transparan, dan tidak dapat dimanipulasi*.


| Role                          | Name                              | NRP        |
|-------------------------------|-----------------------------------|------------|
| Backend & Core Blockchain     | Callista Meyra Azizah             | 5027231060 |
| Security & Digital Signature  | Fadlillah Cantika Sari Hermawan   | 5027231042 |
| Networking & Testing          | Aisyah Rahmasari                  | 5027231072   |

## Fitur Utama Sistem

### Digital Signature (ECDSA)
Menggunakan algoritma Elliptic Curve Digital Signature Algorithm (ECDSA) dengan kurva SECP256k1 untuk memastikan bahwa hanya pemilik Private Key asli yang dapat melakukan absensi.

### Miner Reward
Setiap proses mining akan menghasilkan transaksi tambahan berupa **SYSTEM_REWARD** sebagai bentuk insentif bagi node yang melakukan validasi blok.

### Integritas Data (Anti-Tampering)
Jika data transaksi diubah meskipun hanya satu karakter, maka signature menjadi tidak valid dan transaksi akan ditolak oleh sistem.

---

## Panduan Menjalankan Sistem

### 1. Install Dependency
```bash
pip install flask ecdsa requests
````

---

### 2. Jalankan Server

```bash
python app.py
```

Server akan berjalan di:

```
http://127.0.0.1:5000
```

---

### 3. Generate Identitas Digital

```bash
python wallet.py
```

Output:

```json
{
  "nama": "Tywin Lannister",
  "keterangan": "Hadir",
  "public_key": "...",
  "signature": "..."
}
```

---
## Cara Run:

1. Jalankan ``python app.py``
2. Di Postman, buka tab `POST /transactions/new`. Masukkan nama baru. Klik Send.
3. Lihat pesannya: "Absen (nama) masuk antrian Blok (nomer antrian)".
4. Buka tab `GET /mine.` Klik Send.
5. Lihat Hasilnya: Di hasil Blok (nomer antrian) ini, daftar transactions pasti akan berisi **DUA data: Data (nama) dan Data SYSTEM_REWARD.**

## Dokumentasi (Sebelum menambahkan security):

Hasil `GET /mine` pertama 
<img width="698" height="406" alt="image" src="https://github.com/user-attachments/assets/fe966200-163a-40c5-9f74-fd4f33fa70eb" />

Hasil `GET /chain` pertama 
<img width="698" height="359" alt="image" src="https://github.com/user-attachments/assets/d1e18281-9544-4192-9597-f97c97c2604c" />

Hasil `POST /transactions/new` (absensi baru) 
<img width="701" height="518" alt="image" src="https://github.com/user-attachments/assets/2d48fada-0a62-40af-bd56-1d94b9c977c9" />

Hasil `GET /mine` kedua, menambahkan 1 orang-Tywin Lannister
<img width="701" height="462" alt="image" src="https://github.com/user-attachments/assets/189dc5cf-fafe-462f-bf38-b6028ec623ef" />

Hasil `GET /chain` kedua, menambahka 1 orang-Tywin Lannister
<img width="701" height="532" alt="image" src="https://github.com/user-attachments/assets/326edf55-0166-41f6-a431-93f19bfdbafd" />

## Dokumentasi (Setelah menambahkan security):

1. Identitas Digital didapat dengan Menjalankan wallet.py untuk mendapatkan data otentikasi (Tywin Lannister).
<img width="1241" height="954" alt="image" src="https://github.com/user-attachments/assets/1f033a7c-cf74-4757-a9ff-e80291174191" />

2. Pengujian Penambahan Transaksi Valid (POST) menggunakan url ```http://127.0.0.1:5000/absen```
<img width="1115" height="854" alt="image" src="https://github.com/user-attachments/assets/d15271ce-4be2-486c-8c6c-6b4332af045f" />

3.  Pengujian Validasi Keamanan (POST - Error)
   
Kalau namanya ga sesuai dengan data otentikasi maka absen gagal kara signature nya tidak valid.
<img width="848" height="607" alt="image" src="https://github.com/user-attachments/assets/100767f3-3472-4db1-bbf9-c655bc5c1332" />

4. Pengujian Proses Mining (GET)
   
Data Tywin yang tadi sudah lolos verifikasi ke dalam blockchain. Terlihat hasilnya di bagian transactions, akan terlihat data Tywin Lannister dan SYSTEM_REWARD.
<img width="726" height="625" alt="image" src="https://github.com/user-attachments/assets/b6ecbff4-40fb-451e-952f-a95120c2b3c2" />

5. Menampilkan seluruh chain. Terdapat data Tywin Lannister dengan Signature asli yang rumit, bukan lagi tulisan "DUMMY".
   
<img width="783" height="641" alt="image" src="https://github.com/user-attachments/assets/0ecaad7b-bc45-4345-a4ba-efe240b4f7d3" />
<img width="1092" height="636" alt="image" src="https://github.com/user-attachments/assets/ad9388d9-5ffc-4d01-b859-a66dd9b24404" />
<img width="1245" height="632" alt="image" src="https://github.com/user-attachments/assets/ddc40ca1-0d59-4829-8cda-4b05bd918686" />


---

## Testing Study Cases 

### Persiapan Awal (Prerequisites)

1. Jalankan 3 node pada terminal berbeda:

```bash
python app.py 5000
python app.py 5001
python app.py 5002
```

2. Generate data mahasiswa:

```bash
python wallet.py
```

3. Copy output JSON (contoh: Tywin Lannister)
![alt text](image-14.png)

---

## Study Case 1: Networking (Registrasi Node)

**Tujuan:** Menghubungkan node agar dapat saling berkomunikasi

* Method: `POST`
* URL:

```
http://127.0.0.1:5000/nodes/register
```

* Body (JSON):

```json
{
  "nodes": [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002"
  ]
}
```

* Node berhasil terdaftar
![alt text](image-1.png)

---

## Study Case 2: Penambahan Transaksi Valid 

**Tujuan:** Memastikan absen berhasil jika data valid

* Method: `POST`
* URL:

```
http://127.0.0.1:5000/absen
```

* Body:
  Gunakan JSON dari `wallet.py`

![alt text](image-2.png)

* **Hasil:**
- Transaksi berhasil masuk ke antrian blok
- Response status: 201 Created

---

## Study Case 3: Anti-Titip Absen (Manipulasi Data)

**Tujuan:** Membuktikan sistem menolak manipulasi

**Langkah:**

* Ubah:

```json
"keterangan": "Hadir"
"nama": "Tywin Lannister"
```

menjadi:

```json
"keterangan": "Izin"
"nama": "Tywinn Lannister"
```

* **Jangan ubah signature**

**Ekspektasi:**

* Status: `401 Unauthorized`
* Message:
![alt text](image-3.png)
![alt text](image-15.png)

* **Hasil:**
- Status: 401 Unauthorized
- Status: 403 FORBIDDEN
- Sistem menolak transaksi karena signature tidak sesuai dengan data

---

## Study Case 4: Miner Reward (Insentif Ekonomi)

**Tujuan:** Membuktikan miner mendapat reward

* Method: `GET`
* URL:

```
http://127.0.0.1:5000/mine
```

Lalu cek:

```
http://127.0.0.1:5000/chain
```

**Ekspektasi:**

* Terdapat 2 transaksi:

  * Data mahasiswa
  * `SYSTEM_REWARD` ke `Admin_Node_5000`

![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-8.png)
---

## Study Case 5: Konsensus & Sinkronisasi

**Tujuan:** Membuktikan longest chain rule. Proses ini menggunakan prinsip consensus “Longest Chain Rule”, di mana node dengan chain lebih pendek akan mengadopsi chain yang lebih panjang dan valid dari node lain.

### Langkah langkah

1. Lakukan transaksi dan mining di Node 5000 (Rantai sekarang paling panjang).
2. Cek Node 5001 dan Node 5002, pastikan keduanya masih di blok awal (Blok 1).
3. Lakukan sinkronisasi pada Node 5001: GET http://127.0.0.1:5001/nodes/resolve
![alt text](image-16.png)
4. Lakukan sinkronisasi pada Node 5002: GET http://127.0.0.1:5002/nodes/resolve
![alt text](image-17.png)

Kedua node (5001 & 5002) akan mengadopsi chain dari Node 5000. Ini membuktikan bahwa seluruh jaringan tetap memiliki data yang konsisten meskipun transaksi hanya dilakukan di satu node.

---

## Study Case 6: Integritas Blockchain (Hashing)

**Tujuan:** Membuktikan blok saling terhubung. Pada Study Case 6, kami membuktikan integritas rantai (Chain Integrity). Blok ke-2 menyimpan nilai previous_hash yang berasal dari hash Blok ke-1. Hal ini menunjukkan bahwa setiap blok saling terhubung secara kriptografis. Jika data pada Blok ke-1 diubah, maka hash-nya akan berubah dan menyebabkan ketidaksesuaian dengan previous_hash pada Blok ke-2. Akibatnya, seluruh rantai setelahnya menjadi tidak valid. Inilah yang membuat blockchain bersifat Immutable (tidak dapat diubah)

Selain keterhubungan antar blok, sistem kami juga menjamin integritas data melalui penyimpanan lokal (blockchain_data_port.json). Jika salah satu server mati, sistem akan memuat ulang data dari file ini dan melakukan verifikasi ulang terhadap seluruh hash sebelum server siap melayani transaksi. Hal ini mencegah manipulasi data saat server dalam kondisi offline

* Method: `GET`

```
http://127.0.0.1:5000/chain
```

**Analisis:**

* Bandingkan:

  * `hash` block ke-1
  * `previous_hash` block ke-2

![alt text](image-13.png)

---

## Checklist Pengujian

- [x] Registrasi Node berhasil
- [x] Transaksi valid berhasil masuk
- [x] Manipulasi data ditolak sistem
- [x] Mining menghasilkan reward
- [x] Konsensus antar node berjalan
- [x] Integritas hash terbukti
- [x] Data Persistence: (Data tidak hilang saat server restart karena tersimpan di JSON)

---


