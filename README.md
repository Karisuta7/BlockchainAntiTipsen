*Blockchain Absensi Terverifikasi & Aman*

| Role                          | Name                              | NRP        |
|-------------------------------|-----------------------------------|------------|
| Backend & Core Blockchain     | Callista Meyra Azizah             | 5027231060 |
| Security & Digital Signature  | Fadlillah Cantika Sari Hermawan   | 5027231042 |
| Networking & Testing          | Aisyah Rahmasari                  | 50272310   |

**Cara Run:**

1. Jalankan ``python app.py``
2. Di Postman, buka tab `POST /transactions/new`. Masukkan nama baru. Klik Send.
3. Lihat pesannya: "Absen (nama) masuk antrian Blok (nomer antrian)".
4. Buka tab `GET /mine.` Klik Send.
5. Lihat Hasilnya: Di hasil Blok (nomer antrian) ini, daftar transactions pasti akan berisi **DUA data: Data (nama) dan Data SYSTEM_REWARD.**

**Dokumentasi (sebelum menambahkan security):**

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

**Dokumentasi (Setelah menmbahkan security):**

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


