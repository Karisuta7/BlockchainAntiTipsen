**Pembagian Tugas** (tolong entar dijadiin tabel ya ;-; sama nrpnya juga)

BACKEND & CORE BLOCKCHAIN: Callista Meyra Azizah 5027231060
SECURITY & DIGITAL SIGNATURE : Fadlillah Cantika Sari Hermawan 50272310
NETWORKING & TESTING: Aisyah Rahmasari 50272310

**Cara Run:**

1. Jalankan ``python app.py``
2. Di Postman, buka tab `POST /transactions/new`. Masukkan nama baru. Klik Send.
3. Lihat pesannya: "Absen (nama) masuk antrian Blok (nomer antrian)".
4. Buka tab `GET /mine.` Klik Send.
5. Lihat Hasilnya: Di hasil Blok (nomer antrian) ini, daftar transactions pasti akan berisi **DUA data: Data (nama) dan Data SYSTEM_REWARD.**

**Dokumentasi:**

Hasil `GET /mine` pertama (belum ada security)
<img width="698" height="406" alt="image" src="https://github.com/user-attachments/assets/fe966200-163a-40c5-9f74-fd4f33fa70eb" />

Hasil `GET /chain` pertama (belum ada security)
<img width="698" height="359" alt="image" src="https://github.com/user-attachments/assets/d1e18281-9544-4192-9597-f97c97c2604c" />



Hasil `POST /transactions/new` (absensi baru) pertama (belum ada security)
<img width="701" height="518" alt="image" src="https://github.com/user-attachments/assets/2d48fada-0a62-40af-bd56-1d94b9c977c9" />

Hasil `GET /mine` kedua (belum ada security, menambah 1 orang-Tywin Lannister)
<img width="701" height="462" alt="image" src="https://github.com/user-attachments/assets/189dc5cf-fafe-462f-bf38-b6028ec623ef" />

Hasil `GET /chain` kedua (belum ada security, menambah 1 orang-Tywin Lannister)
<img width="701" height="532" alt="image" src="https://github.com/user-attachments/assets/326edf55-0166-41f6-a431-93f19bfdbafd" />




