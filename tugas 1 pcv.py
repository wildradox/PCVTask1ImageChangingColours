"""
IMAGE LAB - Tugas Pengolahan Citra Digital
============================================
Lingkungan  : Python 3 + numpy + opencv-python + matplotlib
Cara pakai  : jalankan di VS Code (klik Run) atau via terminal:
              python image_lab.py

INSTALASI PAKET (jalankan sekali di terminal VS Code):
    pip install numpy opencv-python matplotlib

Struktur file mengikuti 4 soal:
  1. Uji lingkungan: baca 1 foto & tampilkan
  2. Baca 3 citra (terang, gelap, kontras rendah) -> laporkan shape, dtype, min, max, mean
  3. Cetak potongan 8x8 piksel dari area gelap & terang
  4. Hitung ukuran data mentah vs ukuran file -> rasio kompresi

Fitur tambahan (bonus):
  - Konversi citra ke: Grayscale, Red-scale, Blue-scale, Yellow-scale, Green-scale
  - Dipanggil lewat menu interaktif di bagian bawah skrip
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# SOAL 1 - UJI LINGKUNGAN: BACA 1 FOTO & TAMPILKAN
# =========================================================
def uji_baca_dan_tampilkan(path_gambar):
    """
    Membaca satu gambar dengan OpenCV, lalu men1ampilkannya dengan matplotlib.
    OpenCV membaca gambar dengan urutan channel BGR, sedangkan matplotlib
    menampilkan dengan urutan RGB, sehingga perlu dikonversi dulu.
    """
    img = cv2.imread(path_gambar)  # hasilnya BGR

    if img is None:
        print(f"[GAGAL] Tidak bisa membaca file: {path_gambar}")
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(5, 5))
    plt.imshow(img_rgb)
    plt.title(f"Uji Tampil: {os.path.basename(path_gambar)}")
    plt.axis("off")
    plt.show()

    print(f"[OK] Berhasil membaca & menampilkan: {path_gambar}")
    print(f"     Ukuran (H, W, C): {img.shape}")
    return img


# =========================================================
# SOAL 2 - LAPORAN STATISTIK 3 CITRA (shape, dtype, min, max, mean)
# =========================================================
def laporan_statistik_citra(daftar_path):
    """
    Membaca beberapa citra (mis. terang, gelap, kontras rendah)
    dan mencetak shape, dtype, nilai minimum, maksimum, dan rata-rata piksel.
    """
    print("\n" + "=" * 60)
    print("SOAL 2 - LAPORAN STATISTIK CITRA")
    print("=" * 60)

    hasil = {}
    for path in daftar_path:
        img = cv2.imread(path)
        if img is None:
            print(f"[GAGAL] Tidak bisa membaca: {path}")
            continue

        nama = os.path.basename(path)
        shape = img.shape
        dtype = img.dtype
        nilai_min = img.min()
        nilai_max = img.max()
        nilai_mean = img.mean()

        print(f"\nCitra   : {nama}")
        print(f"  shape : {shape}")
        print(f"  dtype : {dtype}")
        print(f"  min   : {nilai_min}")
        print(f"  max   : {nilai_max}")
        print(f"  mean  : {nilai_mean:.2f}")

        hasil[nama] = {
            "img": img,
            "shape": shape,
            "dtype": dtype,
            "min": nilai_min,
            "max": nilai_max,
            "mean": nilai_mean,
        }

    return hasil


# =========================================================
# SOAL 3 - POTONGAN 8x8 PIKSEL DARI AREA GELAP & TERANG
# =========================================================
def cetak_patch_8x8(img, baris_awal, kolom_awal, label=""):
    """
    Mengambil dan mencetak potongan (patch) 8x8 piksel dari sebuah citra,
    dimulai dari koordinat (baris_awal, kolom_awal).
    Untuk citra berwarna, dicetak per channel (B, G, R) agar mudah dibaca.
    """
    patch = img[baris_awal:baris_awal + 8, kolom_awal:kolom_awal + 8]

    print(f"\n--- Patch 8x8 [{label}] mulai (baris={baris_awal}, kolom={kolom_awal}) ---")
    print(f"Bentuk patch: {patch.shape}")

    if patch.ndim == 3:  # citra berwarna (H, W, 3) -> urutan BGR
        nama_channel = ["Blue", "Green", "Red"]
        for i, nama in enumerate(nama_channel):
            print(f"\nChannel {nama}:")
            print(patch[:, :, i])
    else:  # citra grayscale
        print(patch)

    print(f"\nRentang nilai pada patch ini: min={patch.min()}, max={patch.max()}")
    return patch


def cari_titik_gelap_dan_terang(img):
    """
    Mencari koordinat piksel paling gelap dan paling terang pada citra
    (berdasarkan citra grayscale-nya), untuk dijadikan pusat pengambilan patch.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    idx_gelap = np.unravel_index(np.argmin(gray), gray.shape)
    idx_terang = np.unravel_index(np.argmax(gray), gray.shape)
    return idx_gelap, idx_terang


def soal3_area_gelap_terang(img, nama_citra="citra"):
    print("\n" + "=" * 60)
    print(f"SOAL 3 - PATCH 8x8 AREA GELAP & TERANG ({nama_citra})")
    print("=" * 60)

    (r_gelap, c_gelap), (r_terang, c_terang) = cari_titik_gelap_dan_terang(img)

    # geser sedikit agar patch 8x8 tidak keluar batas gambar
    r_gelap = min(max(r_gelap, 0), img.shape[0] - 8)
    c_gelap = min(max(c_gelap, 0), img.shape[1] - 8)
    r_terang = min(max(r_terang, 0), img.shape[0] - 8)
    c_terang = min(max(c_terang, 0), img.shape[1] - 8)

    cetak_patch_8x8(img, r_gelap, c_gelap, label="area gelap")
    cetak_patch_8x8(img, r_terang, c_terang, label="area terang")


# =========================================================
# SOAL 4 - UKURAN DATA MENTAH vs UKURAN FILE -> RASIO KOMPRESI
# =========================================================
def hitung_rasio_kompresi(path_gambar):
    """
    Menghitung ukuran data mentah citra (uncompressed, dalam byte) berdasarkan
    shape dan dtype array numpy, dibandingkan dengan ukuran file aslinya di disk
    (yang biasanya sudah terkompresi, mis. JPEG/PNG).
    """
    print("\n" + "=" * 60)
    print(f"SOAL 4 - RASIO KOMPRESI: {os.path.basename(path_gambar)}")
    print("=" * 60)

    img = cv2.imread(path_gambar)
    if img is None:
        print(f"[GAGAL] Tidak bisa membaca: {path_gambar}")
        return None

    tinggi, lebar, channel = img.shape
    byte_per_piksel = img.dtype.itemsize  # umumnya 1 byte (uint8)

    # Ukuran data mentah = tinggi x lebar x channel x byte_per_piksel
    ukuran_mentah = tinggi * lebar * channel * byte_per_piksel

    # Ukuran file asli di disk (sudah terkompresi oleh format JPEG/PNG dst.)
    ukuran_file = os.path.getsize(path_gambar)

    rasio = ukuran_mentah / ukuran_file if ukuran_file > 0 else float("inf")

    print(f"Dimensi citra          : {tinggi} x {lebar} x {channel}")
    print(f"Byte per piksel        : {byte_per_piksel}")
    print(f"Ukuran data mentah     : {ukuran_mentah:,} byte  (~{ukuran_mentah/1024:.1f} KB)")
    print(f"Ukuran file di disk    : {ukuran_file:,} byte  (~{ukuran_file/1024:.1f} KB)")
    print(f"Rasio kompresi         : {rasio:.2f} : 1")
    print("(Artinya file di disk kira-kira " f"{rasio:.1f}x lebih kecil dibanding data mentahnya)")

    return {
        "ukuran_mentah": ukuran_mentah,
        "ukuran_file": ukuran_file,
        "rasio": rasio,
    }


# =========================================================
# BONUS - KONVERSI WARNA: GRAYSCALE, RED, BLUE, YELLOW, GREEN
# =========================================================
def ke_grayscale(img):
    """Mengubah citra BGR menjadi grayscale, lalu dikembalikan dalam 3 channel
    (agar bisa ditampilkan/disimpan sejajar dengan citra warna lain)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def ke_redscale(img):
    """Menonjolkan channel Red saja: channel Blue & Green dinolkan."""
    hasil = img.copy()
    hasil[:, :, 0] = 0  # Blue -> 0
    hasil[:, :, 1] = 0  # Green -> 0
    return hasil


def ke_bluescale(img):
    """Menonjolkan channel Blue saja: channel Green & Red dinolkan."""
    hasil = img.copy()
    hasil[:, :, 1] = 0  # Green -> 0
    hasil[:, :, 2] = 0  # Red -> 0
    return hasil


def ke_greenscale(img):
    """Menonjolkan channel Green saja: channel Blue & Red dinolkan."""
    hasil = img.copy()
    hasil[:, :, 0] = 0  # Blue -> 0
    hasil[:, :, 2] = 0  # Red -> 0
    return hasil


def ke_yellowscale(img):
    """
    Kuning = campuran Red + Green (tanpa Blue), karena tidak ada channel
    'yellow' langsung di BGR. Maka channel Blue dinolkan, Red & Green tetap.
    """
    hasil = img.copy()
    hasil[:, :, 0] = 0  # Blue -> 0, sisakan Green & Red -> tampak kuning
    return hasil


KONVERSI_WARNA = {
    "1": ("Grayscale", ke_grayscale),
    "2": ("Red-scale", ke_redscale),
    "3": ("Blue-scale", ke_bluescale),
    "4": ("Yellow-scale", ke_yellowscale),
    "5": ("Green-scale", ke_greenscale),
}


def tampilkan_perbandingan(img_asli, img_hasil, judul_hasil):
    """Menampilkan citra asli dan citra hasil konversi berdampingan."""
    asli_rgb = cv2.cvtColor(img_asli, cv2.COLOR_BGR2RGB)
    hasil_rgb = cv2.cvtColor(img_hasil, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(asli_rgb)
    ax[0].set_title("Asli")
    ax[0].axis("off")

    ax[1].imshow(hasil_rgb)
    ax[1].set_title(judul_hasil)
    ax[1].axis("off")

    plt.tight_layout()
    plt.show()


def menu_konversi_warna(path_gambar):
    img = cv2.imread(path_gambar)
    if img is None:
        print(f"[GAGAL] Tidak bisa membaca: {path_gambar}")
        return

    print("\n" + "=" * 60)
    print("BONUS - KONVERSI WARNA CITRA")
    print("=" * 60)
    for kunci, (nama, _) in KONVERSI_WARNA.items():
        print(f"  {kunci}. {nama}")
    print("  0. Kembali / lewati")

    pilihan = input("Pilih mode konversi (0-5): ").strip()

    if pilihan == "0" or pilihan not in KONVERSI_WARNA:
        print("Dilewati.")
        return

    nama_mode, fungsi = KONVERSI_WARNA[pilihan]
    hasil = fungsi(img)

    tampilkan_perbandingan(img, hasil, nama_mode)

    nama_file = os.path.splitext(os.path.basename(path_gambar))[0]
    output_path = f"{nama_file}_{nama_mode.lower().replace('-', '')}.png"
    cv2.imwrite(output_path, hasil)
    print(f"[OK] Hasil konversi disimpan sebagai: {output_path}")


# =========================================================
# PROGRAM UTAMA
# =========================================================
if __name__ == "__main__":
    # -----------------------------------------------------
    # UBAH DAFTAR PATH INI SESUAI FILE GAMBAR ANDA
    # Sediakan 3 citra: 1 terang, 1 gelap, 1 kontras rendah
    # -----------------------------------------------------
    PATH_TERANG = "gambar_terang.jpg"
    PATH_GELAP = "gambar_gelap.jpg"
    PATH_KONTRAS_RENDAH = "gambar_kontras_rendah.jpg"

    daftar_citra = [PATH_TERANG, PATH_GELAP, PATH_KONTRAS_RENDAH]

    print("#" * 60)
    print("# SOAL 1 - UJI LINGKUNGAN: BACA & TAMPILKAN 1 FOTO")
    print("#" * 60)
    img_uji = uji_baca_dan_tampilkan(PATH_TERANG)

    # SOAL 2
    hasil_statistik = laporan_statistik_citra(daftar_citra)

    # SOAL 3 - lakukan untuk citra gelap & citra terang
    if PATH_TERANG in [os.path.basename(p) for p in hasil_statistik] or os.path.exists(PATH_TERANG):
        img_terang = cv2.imread(PATH_TERANG)
        if img_terang is not None:
            soal3_area_gelap_terang(img_terang, nama_citra=PATH_TERANG)

    if os.path.exists(PATH_GELAP):
        img_gelap = cv2.imread(PATH_GELAP)
        if img_gelap is not None:
            soal3_area_gelap_terang(img_gelap, nama_citra=PATH_GELAP)

    # SOAL 4 - hitung rasio kompresi salah satu citra
    if os.path.exists(PATH_TERANG):
        hitung_rasio_kompresi(PATH_TERANG)

    # BONUS - menu konversi warna interaktif
    if os.path.exists(PATH_TERANG):
        menu_konversi_warna(PATH_TERANG)

    print("\nSelesai. Semua tahapan tugas telah dijalankan.")
