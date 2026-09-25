"""
2-ti-eq.py
=========================================================
TRANSFORMASI INTENSITAS & EKUALISASI HISTOGRAM
=========================================================
Aturan tugas: DILARANG memakai fungsi bawaan package untuk
proses pengolahan citranya. Artinya TIDAK memakai:
    - cv2.equalizeHist()
    - cv2.LUT()
    - cv2.convertScaleAbs()
    - np.histogram() / np.bincount()
    - cv2.cvtColor() untuk grayscale
Semua transformasi & histogram dihitung manual pakai numpy
array + operasi matematika dasar. cv2.imread / cv2.imwrite /
matplotlib hanya dipakai untuk BACA & TAMPILKAN, bukan proses.

Cara pakai:
    pip install numpy opencv-python matplotlib
    python 2-ti-eq.py
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# 0. UTILITAS DASAR (baca gambar, konversi grayscale manual)
# =========================================================
def baca_grayscale_manual(path_gambar):
    """
    Membaca citra berwarna, lalu mengubahnya ke grayscale SECARA MANUAL
    memakai rumus luminance standar:
        gray = 0.299*R + 0.587*G + 0.114*B
    (bukan cv2.cvtColor).
    """
    img_bgr = cv2.imread(path_gambar)
    if img_bgr is None:
        raise FileNotFoundError(f"Tidak bisa membaca file: {path_gambar}")

    # OpenCV membaca dalam urutan B, G, R
    b = img_bgr[:, :, 0].astype(np.float64)
    g = img_bgr[:, :, 1].astype(np.float64)
    r = img_bgr[:, :, 2].astype(np.float64)

    gray = 0.299 * r + 0.587 * g + 0.114 * b
    gray = np.clip(gray, 0, 255).astype(np.uint8)

    return gray


# =========================================================
# 1. TRANSFORMASI INTENSITAS (point processing)
# =========================================================
def transformasi_negatif(img):
    """
    Transformasi negatif: s = (L-1) - r
    Membalik terang menjadi gelap dan sebaliknya.
    """
    L = 256
    hasil = (L - 1) - img.astype(np.int32)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def transformasi_log(img, c=None):
    """
    Transformasi log: s = c * log(1 + r)
    Memperjelas detail pada area gelap, menekan area terang.
    Jika c tidak diberikan, dihitung otomatis agar hasil pas di 0-255.
    """
    img_f = img.astype(np.float64)

    if c is None:
        # supaya nilai maksimum hasil tepat 255
        c = 255.0 / np.log(1 + img_f.max())

    hasil = c * np.log(1 + img_f)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def transformasi_power_law(img, gamma, c=None):
    """
    Transformasi power-law (gamma correction): s = c * r^gamma
    gamma < 1 -> gambar jadi lebih terang
    gamma > 1 -> gambar jadi lebih gelap
    """
    img_f = img.astype(np.float64) / 255.0  # normalisasi ke 0-1

    if c is None:
        c = 1.0

    hasil = c * np.power(img_f, gamma)
    hasil = hasil * 255.0
    return np.clip(hasil, 0, 255).astype(np.uint8)


def peregangan_kontras(img, r1, s1, r2, s2):
    """
    Contrast stretching piecewise-linear dengan 2 titik kontrol (r1,s1) dan (r2,s2).

    Tiga segmen linear:
        0   <= r < r1  : s = (s1/r1) * r                      (jika r1 > 0)
        r1  <= r < r2  : s = ((s2-s1)/(r2-r1)) * (r-r1) + s1
        r2  <= r <= 255: s = ((255-s2)/(255-r2)) * (r-r2) + s2 (jika r2 < 255)
    """
    img_f = img.astype(np.float64)
    hasil = np.zeros_like(img_f)

    # Segmen 1: 0 sampai r1
    mask1 = img_f < r1
    if r1 > 0:
        hasil[mask1] = (s1 / r1) * img_f[mask1]

    # Segmen 2: r1 sampai r2
    mask2 = (img_f >= r1) & (img_f < r2)
    if r2 != r1:
        hasil[mask2] = ((s2 - s1) / (r2 - r1)) * (img_f[mask2] - r1) + s1

    # Segmen 3: r2 sampai 255
    mask3 = img_f >= r2
    if r2 != 255:
        hasil[mask3] = ((255 - s2) / (255 - r2)) * (img_f[mask3] - r2) + s2
    else:
        hasil[mask3] = s2

    return np.clip(hasil, 0, 255).astype(np.uint8)


# =========================================================
# 2. HISTOGRAM MANUAL (tanpa np.histogram / cv2.calcHist)
# =========================================================
def hitung_histogram_manual(img):
    """
    Menghitung histogram (jumlah kemunculan tiap level intensitas 0-255)
    secara manual, tanpa np.histogram() / np.bincount() / cv2.calcHist().
    """
    histogram = np.zeros(256, dtype=np.int64)

    for level in range(256):
        # menghitung berapa piksel yang nilainya persis = level
        histogram[level] = np.sum(img == level)

    return histogram


def hitung_pdf(histogram, total_piksel):
    """Probability Density Function: histogram dibagi total piksel."""
    return histogram / total_piksel


def hitung_cdf_manual(pdf):
    """
    Cumulative Distribution Function, dihitung manual dengan
    akumulasi satu per satu (bukan np.cumsum).
    """
    cdf = np.zeros(256, dtype=np.float64)
    akumulasi = 0.0

    for level in range(256):
        akumulasi += pdf[level]
        cdf[level] = akumulasi

    return cdf


# =========================================================
# 3. EKUALISASI HISTOGRAM MANUAL
# =========================================================
def ekualisasi_histogram_manual(img):
    """
    Ekualisasi histogram klasik:
        1. Hitung histogram
        2. Hitung PDF
        3. Hitung CDF
        4. Petakan CDF ke rentang 0-255 -> lookup table (LUT)
        5. Terapkan LUT ke tiap piksel (tanpa cv2.LUT, pakai indexing manual)
    """
    tinggi, lebar = img.shape
    total_piksel = tinggi * lebar

    histogram = hitung_histogram_manual(img)
    pdf = hitung_pdf(histogram, total_piksel)
    cdf = hitung_cdf_manual(pdf)

    # Petakan CDF (0..1) ke level intensitas baru (0..255)
    lut = np.round(cdf * 255).astype(np.uint8)

    # Terapkan LUT manual ke setiap piksel (loop per level, bukan cv2.LUT)
    hasil = np.zeros_like(img)
    for level in range(256):
        hasil[img == level] = lut[level]

    return hasil, histogram, lut


# =========================================================
# 4. VISUALISASI
# =========================================================
def tampilkan_citra_dan_histogram(daftar_citra, daftar_judul):
    """
    Menampilkan beberapa citra beserta histogramnya masing-masing,
    disusun 2 baris (baris atas = citra, baris bawah = histogram).
    """
    n = len(daftar_citra)
    fig, ax = plt.subplots(2, n, figsize=(4 * n, 7))

    for i in range(n):
        img = daftar_citra[i]
        judul = daftar_judul[i]
        hist = hitung_histogram_manual(img)

        ax[0, i].imshow(img, cmap="gray", vmin=0, vmax=255)
        ax[0, i].set_title(judul)
        ax[0, i].axis("off")

        ax[1, i].bar(range(256), hist, width=1.0, color="gray")
        ax[1, i].set_title(f"Histogram: {judul}")
        ax[1, i].set_xlim([0, 255])

    plt.tight_layout()
    plt.show()


# =========================================================
# PROGRAM UTAMA
# =========================================================
if __name__ == "__main__":
    # -----------------------------------------------------
    # UBAH PATH INI SESUAI FILE GAMBAR ANDA
    # -----------------------------------------------------
    PATH_GAMBAR = "gambar_kontras_rendah.jpg"

    img_gray = baca_grayscale_manual(PATH_GAMBAR)
    print(f"Citra dibaca: {PATH_GAMBAR}  shape={img_gray.shape}  dtype={img_gray.dtype}")

    # ---------------- TRANSFORMASI INTENSITAS ----------------
    print("\nMenerapkan transformasi intensitas...")

    img_negatif = transformasi_negatif(img_gray)
    img_log = transformasi_log(img_gray)
    img_gamma_terang = transformasi_power_law(img_gray, gamma=0.5)   # lebih terang
    img_gamma_gelap = transformasi_power_law(img_gray, gamma=2.0)    # lebih gelap
    img_stretch = peregangan_kontras(img_gray, r1=70, s1=0, r2=180, s2=255)

    tampilkan_citra_dan_histogram(
        [img_gray, img_negatif, img_log],
        ["Asli", "Negatif", "Log"],
    )
    tampilkan_citra_dan_histogram(
        [img_gray, img_gamma_terang, img_gamma_gelap, img_stretch],
        ["Asli", "Gamma 0.5 (terang)", "Gamma 2.0 (gelap)", "Contrast Stretch"],
    )

    # ---------------- EKUALISASI HISTOGRAM ----------------
    print("\nMenerapkan ekualisasi histogram...")

    img_eq, hist_asli, lut = ekualisasi_histogram_manual(img_gray)

    print("\nContoh pemetaan LUT (level asli -> level baru):")
    for level in [0, 50, 100, 128, 150, 200, 255]:
        print(f"  {level:3d} -> {lut[level]:3d}")

    tampilkan_citra_dan_histogram(
        [img_gray, img_eq],
        ["Sebelum Ekualisasi", "Sesudah Ekualisasi"],
    )

    # Simpan hasil ke file
    cv2.imwrite("hasil_negatif.png", img_negatif)
    cv2.imwrite("hasil_log.png", img_log)
    cv2.imwrite("hasil_ekualisasi.png", img_eq)
    print("\n[OK] Hasil disimpan: hasil_negatif.png, hasil_log.png, hasil_ekualisasi.png")

    print("\nSelesai.")
