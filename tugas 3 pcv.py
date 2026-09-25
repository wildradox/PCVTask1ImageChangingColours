"""
3-filter-spasial.py
=========================================================
FILTER SPASIAL (SPATIAL FILTERING)
=========================================================
Implementasi konvolusi 2D secara MANUAL (tanpa cv2.filter2D,
cv2.GaussianBlur, cv2.medianBlur, cv2.Sobel, cv2.Laplacian),
supaya jelas terlihat mekanisme filter spasial itu sendiri.

Filter yang didemonstrasikan:
  1. Smoothing / Blur   -> Mean filter (average) & Gaussian filter
  2. Sharpening         -> Kernel penajaman
  3. Edge Detection     -> Sobel (X & Y + magnitude) dan Laplacian
  4. Median filter      -> non-linear, bukan konvolusi (untuk noise salt & pepper)

Cara pakai:
    pip install numpy opencv-python matplotlib
    python 3-filter-spasial.py
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 0. UTILITAS: BACA GRAYSCALE MANUAL & PADDING MANUAL
# =========================================================
def baca_grayscale_manual(path_gambar):
    """Baca citra & ubah ke grayscale manual (rumus luminance), bukan cv2.cvtColor."""
    img_bgr = cv2.imread(path_gambar)
    if img_bgr is None:
        raise FileNotFoundError(f"Tidak bisa membaca file: {path_gambar}")

    b = img_bgr[:, :, 0].astype(np.float64)
    g = img_bgr[:, :, 1].astype(np.float64)
    r = img_bgr[:, :, 2].astype(np.float64)

    gray = 0.299 * r + 0.587 * g + 0.114 * b
    return np.clip(gray, 0, 255).astype(np.uint8)


def tambah_padding(img, pad):
    """
    Zero-padding manual di sekeliling citra sebanyak `pad` piksel
    (bukan cv2.copyMakeBorder), agar konvolusi bisa menjangkau tepi gambar.
    """
    tinggi, lebar = img.shape
    hasil = np.zeros((tinggi + 2 * pad, lebar + 2 * pad), dtype=np.float64)
    hasil[pad:pad + tinggi, pad:pad + lebar] = img.astype(np.float64)
    return hasil


# =========================================================
# 1. KONVOLUSI 2D MANUAL (INTI FILTER SPASIAL)
# =========================================================
def konvolusi_2d(img, kernel):
    """
    Konvolusi 2D manual antara citra grayscale dan sebuah kernel.

    Untuk tiap piksel output, kernel "digeser" (sliding window) di atas
    citra, dikalikan elemen-per-elemen dengan area piksel di sekitarnya,
    lalu dijumlahkan -> itulah nilai piksel hasil.

    Catatan: ini konvolusi sesuai definisi pemrosesan citra (yang secara
    matematis sebenarnya "cross-correlation", kernel tidak dibalik -
    umum dipakai di kuliah pengolahan citra).
    """
    tinggi_k, lebar_k = kernel.shape
    pad_h = tinggi_k // 2
    pad_w = lebar_k // 2

    img_pad = tambah_padding(img, max(pad_h, pad_w))
    tinggi, lebar = img.shape

    hasil = np.zeros((tinggi, lebar), dtype=np.float64)

    for i in range(tinggi):
        for j in range(lebar):
            # ambil area (patch) seukuran kernel, di sekitar piksel (i, j)
            area = img_pad[i:i + tinggi_k, j:j + lebar_k]
            hasil[i, j] = np.sum(area * kernel)

    return hasil


def normalisasi_ke_uint8(img_float):
    """Clip ke 0-255 dan ubah ke uint8 supaya bisa ditampilkan/disimpan."""
    return np.clip(img_float, 0, 255).astype(np.uint8)


# =========================================================
# 2. FILTER SMOOTHING (BLUR)
# =========================================================
def buat_kernel_mean(ukuran=3):
    """Mean filter / average filter: semua bobot sama, jumlah = 1."""
    return np.ones((ukuran, ukuran), dtype=np.float64) / (ukuran * ukuran)


def buat_kernel_gaussian(ukuran=5, sigma=1.0):
    """
    Kernel Gaussian dibuat manual dari rumus 2D Gaussian:
        G(x,y) = exp(-(x^2+y^2) / (2*sigma^2))
    lalu dinormalisasi supaya total bobotnya = 1.
    """
    ax = np.arange(-(ukuran // 2), ukuran // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    kernel = kernel / np.sum(kernel)
    return kernel


def filter_median_manual(img, ukuran=3):
    """
    Median filter: non-linear, BUKAN konvolusi (tidak ada perkalian kernel).
    Tiap piksel diganti dengan nilai median dari tetangganya.
    Ampuh untuk noise salt & pepper, sekaligus mempertahankan tepi lebih baik
    dibanding mean filter.
    """
    pad = ukuran // 2
    img_pad = tambah_padding(img, pad)
    tinggi, lebar = img.shape

    hasil = np.zeros((tinggi, lebar), dtype=np.float64)

    for i in range(tinggi):
        for j in range(lebar):
            area = img_pad[i:i + ukuran, j:j + ukuran]
            hasil[i, j] = np.median(area)

    return normalisasi_ke_uint8(hasil)


# =========================================================
# 3. FILTER SHARPENING (PENAJAMAN)
# =========================================================
def buat_kernel_sharpen():
    """
    Kernel penajaman klasik: menonjolkan pusat piksel relatif terhadap
    tetangganya (unsharp masking sederhana).
    """
    return np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ], dtype=np.float64)


# =========================================================
# 4. FILTER EDGE DETECTION
# =========================================================
def buat_kernel_sobel_x():
    """Sobel X: mendeteksi tepi vertikal (perubahan intensitas horizontal)."""
    return np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ], dtype=np.float64)


def buat_kernel_sobel_y():
    """Sobel Y: mendeteksi tepi horizontal (perubahan intensitas vertikal)."""
    return np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1],
    ], dtype=np.float64)


def buat_kernel_laplacian():
    """Laplacian: turunan kedua, mendeteksi tepi di segala arah sekaligus."""
    return np.array([
        [0,  1, 0],
        [1, -4, 1],
        [0,  1, 0],
    ], dtype=np.float64)


def deteksi_tepi_sobel(img):
    """
    Menjalankan Sobel X dan Sobel Y, lalu menggabungkan menjadi
    magnitude gradien: G = sqrt(Gx^2 + Gy^2)
    """
    gx = konvolusi_2d(img, buat_kernel_sobel_x())
    gy = konvolusi_2d(img, buat_kernel_sobel_y())

    magnitude = np.sqrt(gx**2 + gy**2)

    return normalisasi_ke_uint8(gx), normalisasi_ke_uint8(gy), normalisasi_ke_uint8(magnitude)


# =========================================================
# 5. VISUALISASI
# =========================================================
def tampilkan_perbandingan(daftar_citra, daftar_judul, kolom=3):
    n = len(daftar_citra)
    baris = int(np.ceil(n / kolom))

    fig, ax = plt.subplots(baris, kolom, figsize=(4 * kolom, 4 * baris))
    ax = np.array(ax).reshape(-1)  # ratakan supaya mudah di-loop

    for i in range(n):
        ax[i].imshow(daftar_citra[i], cmap="gray", vmin=0, vmax=255)
        ax[i].set_title(daftar_judul[i])
        ax[i].axis("off")

    # matikan subplot kosong sisa
    for i in range(n, len(ax)):
        ax[i].axis("off")

    plt.tight_layout()
    plt.show()


# =========================================================
# PROGRAM UTAMA
# =========================================================
if __name__ == "__main__":
    # -----------------------------------------------------
    # UBAH PATH INI SESUAI FILE GAMBAR ANDA
    # -----------------------------------------------------
    PATH_GAMBAR = "gambar_terang.jpg"

    img_gray = baca_grayscale_manual(PATH_GAMBAR)
    print(f"Citra dibaca: {PATH_GAMBAR}  shape={img_gray.shape}  dtype={img_gray.dtype}")

    # ---------------- SMOOTHING ----------------
    print("\nMenerapkan filter smoothing...")
    img_mean = normalisasi_ke_uint8(konvolusi_2d(img_gray, buat_kernel_mean(3)))
    img_gaussian = normalisasi_ke_uint8(konvolusi_2d(img_gray, buat_kernel_gaussian(5, sigma=1.0)))
    img_median = filter_median_manual(img_gray, ukuran=3)

    tampilkan_perbandingan(
        [img_gray, img_mean, img_gaussian, img_median],
        ["Asli", "Mean Filter 3x3", "Gaussian Filter 5x5", "Median Filter 3x3"],
    )

    # ---------------- SHARPENING ----------------
    print("Menerapkan filter sharpening...")
    img_sharpen = normalisasi_ke_uint8(konvolusi_2d(img_gray, buat_kernel_sharpen()))

    tampilkan_perbandingan(
        [img_gray, img_sharpen],
        ["Asli", "Sharpening"],
    )

    # ---------------- EDGE DETECTION ----------------
    print("Menerapkan filter edge detection...")
    sobel_x, sobel_y, sobel_mag = deteksi_tepi_sobel(img_gray)
    img_laplacian = normalisasi_ke_uint8(konvolusi_2d(img_gray, buat_kernel_laplacian()))

    tampilkan_perbandingan(
        [img_gray, sobel_x, sobel_y, sobel_mag, img_laplacian],
        ["Asli", "Sobel X", "Sobel Y", "Sobel Magnitude", "Laplacian"],
    )

    # ---------------- SIMPAN HASIL ----------------
    cv2.imwrite("hasil_mean.png", img_mean)
    cv2.imwrite("hasil_gaussian.png", img_gaussian)
    cv2.imwrite("hasil_median.png", img_median)
    cv2.imwrite("hasil_sharpen.png", img_sharpen)
    cv2.imwrite("hasil_sobel_magnitude.png", sobel_mag)
    cv2.imwrite("hasil_laplacian.png", img_laplacian)
    print("\n[OK] Semua hasil filter disimpan sebagai file PNG.")

    print("\nSelesai.")
