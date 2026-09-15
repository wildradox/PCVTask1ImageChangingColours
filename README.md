# PCVTask1ImageChangingColours
# IMAGE LAB — Tugas Pengolahan Citra Digital

Program Python sederhana untuk mengerjakan tugas **Pengolahan Citra Digital** menggunakan **NumPy, OpenCV, dan Matplotlib**.

Program ini mencakup pembacaan dan visualisasi citra, analisis statistik piksel, pengambilan patch 8×8 dari area gelap dan terang, perhitungan rasio kompresi, serta fitur bonus berupa konversi warna.

---

## 📋 Daftar Isi

* [Deskripsi](#-deskripsi)
* [Fitur](#-fitur)
* [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
* [Struktur Folder](#-struktur-folder)
* [Instalasi](#-instalasi)
* [Persiapan File Gambar](#-persiapan-file-gambar)
* [Cara Menjalankan Program](#-cara-menjalankan-program)
* [Penjelasan Soal](#-penjelasan-soal)
* [Fitur Bonus](#-fitur-bonus)
* [Contoh Output](#-contoh-output)
* [Catatan](#-catatan)
* [Lisensi](#-lisensi)

---

## 📖 Deskripsi

**IMAGE LAB** adalah program untuk melakukan beberapa operasi dasar pengolahan citra digital menggunakan Python.

Program menggunakan **OpenCV** untuk membaca dan memproses gambar, **NumPy** untuk melakukan analisis data piksel, serta **Matplotlib** untuk menampilkan gambar.

Tugas utama yang dikerjakan terdiri dari 4 bagian:

1. Menguji lingkungan dengan membaca dan menampilkan satu foto.
2. Membaca tiga citra dan menampilkan statistiknya.
3. Mengambil potongan piksel berukuran 8×8 dari area gelap dan terang.
4. Membandingkan ukuran data mentah dengan ukuran file untuk menghitung rasio kompresi.

Selain itu, terdapat fitur bonus untuk melakukan konversi citra ke beberapa mode warna.

---

## ✨ Fitur

### Soal 1 — Baca dan Tampilkan Citra

Program membaca satu file gambar menggunakan OpenCV kemudian menampilkannya menggunakan Matplotlib.

Karena OpenCV menggunakan format channel **BGR**, sedangkan Matplotlib menggunakan **RGB**, program melakukan konversi terlebih dahulu.

Informasi ukuran gambar juga ditampilkan.

---

### Soal 2 — Statistik Citra

Program dapat membaca tiga citra:

* Citra terang
* Citra gelap
* Citra dengan kontras rendah

Kemudian program menampilkan:

* `shape`
* `dtype`
* nilai minimum piksel
* nilai maksimum piksel
* nilai rata-rata (`mean`)

Contoh informasi:

```text
Citra   : gambar_terang.jpg
  shape : (720, 1280, 3)
  dtype : uint8
  min   : 0
  max   : 255
  mean  : 142.37
```

---

### Soal 3 — Patch 8×8 Piksel

Program mencari:

* piksel paling gelap
* piksel paling terang

Pencarian dilakukan berdasarkan citra grayscale.

Setelah koordinat ditemukan, program mengambil area berukuran **8×8 piksel** di sekitar lokasi tersebut.

Untuk citra berwarna, nilai piksel ditampilkan berdasarkan channel:

* Blue
* Green
* Red

---

### Soal 4 — Rasio Kompresi

Program membandingkan:

1. Ukuran data mentah citra di memori.
2. Ukuran file gambar di disk.

Ukuran data mentah dihitung berdasarkan:

```text
tinggi × lebar × jumlah channel × byte per piksel
```

Kemudian rasio kompresi dihitung dengan rumus:

```text
Rasio Kompresi = Ukuran Data Mentah / Ukuran File
```

Contoh:

```text
Ukuran data mentah     : 2,764,800 byte
Ukuran file di disk    : 345,600 byte
Rasio kompresi         : 8.00 : 1
```

Artinya ukuran file di disk sekitar 8 kali lebih kecil dibandingkan data mentahnya.

---

## 🎨 Fitur Bonus

Program menyediakan beberapa pilihan konversi warna:

| Pilihan | Mode             |
| ------- | ---------------- |
| 1       | Grayscale        |
| 2       | Red-scale        |
| 3       | Blue-scale       |
| 4       | Yellow-scale     |
| 5       | Green-scale      |
| 0       | Kembali / lewati |

### Grayscale

Mengubah citra berwarna menjadi citra grayscale.

### Red-scale

Hanya mempertahankan channel **Red**, sedangkan Blue dan Green dibuat menjadi 0.

### Blue-scale

Hanya mempertahankan channel **Blue**, sedangkan Green dan Red dibuat menjadi 0.

### Green-scale

Hanya mempertahankan channel **Green**, sedangkan Blue dan Red dibuat menjadi 0.

### Yellow-scale

Warna kuning diperoleh dari kombinasi:

```text
Red + Green
```

Oleh karena itu, channel Blue dibuat menjadi 0.

---

## 🛠 Teknologi yang Digunakan

Program dibuat menggunakan:

* **Python 3**
* **NumPy**
* **OpenCV**
* **Matplotlib**

Library yang digunakan di dalam program:

```python
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

---

## 📁 Struktur Folder

Struktur folder yang disarankan:

```text
image-lab/
│
├── image_lab.py
├── README.md
│
├── gambar_terang.jpg
├── gambar_gelap.jpg
└── gambar_kontras_rendah.jpg
```

Keterangan:

| File                        | Fungsi                      |
| --------------------------- | --------------------------- |
| `image_lab.py`              | Program utama               |
| `README.md`                 | Dokumentasi proyek          |
| `gambar_terang.jpg`         | Citra dengan kondisi terang |
| `gambar_gelap.jpg`          | Citra dengan kondisi gelap  |
| `gambar_kontras_rendah.jpg` | Citra dengan kontras rendah |

File hasil konversi warna akan dibuat otomatis oleh program dalam format `.png`.

---

## 💻 Instalasi

Pastikan **Python 3** sudah terpasang di komputer.

Buka terminal pada VS Code, kemudian jalankan:

```bash
pip install numpy opencv-python matplotlib
```

Untuk memastikan library sudah berhasil terpasang, dapat menggunakan:

```bash
pip list
```

Pastikan terdapat:

```text
numpy
opencv-python
matplotlib
```

---

## 🖼 Persiapan File Gambar

Sebelum menjalankan program, siapkan tiga gambar.

### 1. Gambar terang

Simpan dengan nama:

```text
gambar_terang.jpg
```

### 2. Gambar gelap

Simpan dengan nama:

```text
gambar_gelap.jpg
```

### 3. Gambar kontras rendah

Simpan dengan nama:

```text
gambar_kontras_rendah.jpg
```

Ketiga file tersebut sebaiknya diletakkan di folder yang sama dengan `image_lab.py`.

Jika ingin menggunakan nama file berbeda, ubah bagian berikut pada program:

```python
PATH_TERANG = "gambar_terang.jpg"
PATH_GELAP = "gambar_gelap.jpg"
PATH_KONTRAS_RENDAH = "gambar_kontras_rendah.jpg"
```

Contohnya:

```python
PATH_TERANG = "foto_pagi.jpg"
PATH_GELAP = "foto_malam.jpg"
PATH_KONTRAS_RENDAH = "foto_kabut.jpg"
```

---

## ▶️ Cara Menjalankan Program

### Menggunakan VS Code

1. Buka folder proyek di VS Code.
2. Pastikan `image_lab.py` dan file gambar berada di folder yang benar.
3. Buka file `image_lab.py`.
4. Klik tombol **Run Python File**.
5. Program akan mulai menjalankan seluruh tahapan tugas.

### Menggunakan Terminal

Masuk ke folder proyek:

```bash
cd image-lab
```

Kemudian jalankan:

```bash
python image_lab.py
```

Pada beberapa sistem, Python dapat dijalankan dengan:

```bash
python3 image_lab.py
```

---

## 🔄 Alur Program

Secara umum, program berjalan dengan alur berikut:

```text
Mulai
  │
  ▼
Baca & tampilkan gambar terang
  │
  ▼
Analisis statistik 3 gambar
  │
  ▼
Cari area paling gelap & terang
  │
  ▼
Ambil patch 8×8 piksel
  │
  ▼
Hitung rasio kompresi
  │
  ▼
Menu konversi warna
  │
  ▼
Selesai
```

---

## 📊 Contoh Output

Ketika program dijalankan, terminal akan menampilkan informasi seperti:

```text
############################################################
# SOAL 1 - UJI LINGKUNGAN: BACA & TAMPILKAN 1 FOTO
############################################################

[OK] Berhasil membaca & menampilkan: gambar_terang.jpg
     Ukuran (H, W, C): (720, 1280, 3)
```

Kemudian:

```text
============================================================
SOAL 2 - LAPORAN STATISTIK CITRA
============================================================

Citra   : gambar_terang.jpg
  shape : (720, 1280, 3)
  dtype : uint8
  min   : 0
  max   : 255
  mean  : 145.32
```

Untuk soal 3:

```text
============================================================
SOAL 3 - PATCH 8x8 AREA GELAP & TERANG
============================================================

--- Patch 8x8 [area gelap] mulai (baris=100, kolom=200) ---
Bentuk patch: (8, 8, 3)
```

Dan untuk soal 4:

```text
============================================================
SOAL 4 - RASIO KOMPRESI: gambar_terang.jpg
============================================================

Dimensi citra          : 720 x 1280 x 3
Byte per piksel        : 1
Ukuran data mentah     : 2,764,800 byte
Ukuran file di disk    : 412,500 byte
Rasio kompresi         : 6.70 : 1
```

---

## 🧩 Fungsi Utama

Beberapa fungsi utama dalam program:

| Fungsi                          | Kegunaan                               |
| ------------------------------- | -------------------------------------- |
| `uji_baca_dan_tampilkan()`      | Membaca dan menampilkan gambar         |
| `laporan_statistik_citra()`     | Menghitung statistik citra             |
| `cetak_patch_8x8()`             | Mencetak patch 8×8 piksel              |
| `cari_titik_gelap_dan_terang()` | Mencari piksel paling gelap dan terang |
| `soal3_area_gelap_terang()`     | Menjalankan analisis patch             |
| `hitung_rasio_kompresi()`       | Menghitung rasio kompresi              |
| `ke_grayscale()`                | Konversi grayscale                     |
| `ke_redscale()`                 | Konversi red-scale                     |
| `ke_bluescale()`                | Konversi blue-scale                    |
| `ke_yellowscale()`              | Konversi yellow-scale                  |
| `ke_greenscale()`               | Konversi green-scale                   |
| `menu_konversi_warna()`         | Menampilkan menu konversi warna        |

---

## ⚠️ Catatan

1. Pastikan nama file gambar sesuai dengan nama yang terdapat pada variabel `PATH_TERANG`, `PATH_GELAP`, dan `PATH_KONTRAS_RENDAH`.

2. File gambar harus dapat dibaca oleh OpenCV.

3. Untuk soal 3, ukuran gambar sebaiknya minimal **8×8 piksel**, karena program mengambil patch berukuran 8×8.

4. OpenCV membaca gambar berwarna dalam format **BGR**, bukan RGB.

5. Nilai piksel pada gambar bertipe `uint8` berada pada rentang:

```text
0 — 255
```

6. Rasio kompresi yang dihitung merupakan perbandingan ukuran array citra yang telah didekodekan dengan ukuran file gambar di disk. Nilainya bukan metrik kualitas kompresi JPEG/PNG secara khusus.

7. Hasil konversi warna akan disimpan otomatis sebagai file `.png` di folder tempat program dijalankan.

---

## 👨‍💻 Tujuan Pembelajaran

Melalui proyek ini, pengguna diharapkan dapat memahami dasar-dasar:

* Pembacaan citra menggunakan OpenCV.
* Representasi citra sebagai array NumPy.
* Dimensi dan tipe data citra.
* Nilai piksel dan channel warna.
* Konversi BGR ke RGB.
* Konversi citra ke grayscale.
* Analisis area gelap dan terang.
* Pengambilan subset/patch piksel.
* Perhitungan ukuran data mentah.
* Konsep dasar kompresi citra.
* Manipulasi channel warna pada citra digital.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan **pembelajaran dan**
