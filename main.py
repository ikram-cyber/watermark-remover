import cv2
import numpy as np
import argparse
import sys
import os

def remove_watermark(image_path, output_path, x, y, w, h):
    print(f"[!] Memproses gambar: {image_path}")
    
    # Baca gambar
    img = cv2.imread(image_path)
    if img is None:
        print("[-] Error: Gambar tidak ditemukan atau format tidak didukung!")
        sys.exit(1)

    # Bikin mask (kanvas hitam)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # Gambar kotak putih di area watermark (x, y, lebar, tinggi)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

    print("[!] Menambal area watermark dengan algoritma Inpainting...")
    # Proses inpainting (Radius 3, Algoritma TELEA)
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    # Simpan hasil
    cv2.imwrite(output_path, result)
    print(f"[+] Sukses! Ahli foto melongo melihat hasilnya di: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aplikasi Hapus Watermark CLI - Termux Edition")
    parser.add_argument("-i", "--image", required=True, help="Path gambar asli")
    parser.add_argument("-o", "--output", default="hasil_tanpa_watermark.jpg", help="Path gambar output (opsional)")
    parser.add_argument("-x", type=int, required=True, help="Titik X (kiri ke kanan) mulai watermark")
    parser.add_argument("-y", type=int, required=True, help="Titik Y (atas ke bawah) mulai watermark")
    parser.add_argument("-w", "--width", type=int, required=True, help="Lebar area watermark")
    parser.add_argument("-l", "--length", type=int, required=True, dest="height", help="Tinggi area watermark")

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[-] Error: File '{args.image}' tidak ada!")
        sys.exit(1)

    remove_watermark(args.image, args.output, args.x, args.y, args.width, args.height)
