"""
PDF-X: Enterprise PDF Utility Tool (Ultimate Edition v3.4)
Fitur: Merge, Split, Compress (Hyper-Aggressive), Image-to-PDF, PDF-to-Image, Security.
Plus: Support Menu, Compact Log UI, Smart Compression Presets, Metadata Cleaner.
Author: Assistant
License: Open Source
"""

import os
import sys
import threading
import base64
import time
import gc
import ctypes
import webbrowser  # Added for Support Link
from datetime import datetime
from io import BytesIO

# UI & Interaction
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from PIL import Image

# Backend Logic
import fitz  # PyMuPDF

# --- KONFIGURASI SISTEM ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# High DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# --- FONT CONFIG ---
FONTS = {
    "h1": ("Arial", 32, "bold"),
    "h2": ("Arial", 24, "bold"),
    "h3": ("Arial", 18, "bold"),
    "body": ("Arial", 14),
    "body_small": ("Arial", 12),
    "btn": ("Arial", 16, "bold"),
    "log": ("Consolas", 11)
}

# --- KAMUS BAHASA ---
LANG = {
    "ID": {
        "app_title": "PDF-X | Enterprise Tool",
        "sidebar_title": "PDF-X",
        "sidebar_sub": "v3.4 Ultimate",
        "nav_merge": " Gabung PDF",
        "nav_split": " Pisah PDF",
        "nav_comp": " Kompres",
        "nav_i2p": " Gambar ke PDF",
        "nav_p2i": " PDF ke Gambar",
        "nav_sec": " Keamanan",
        "btn_add": "➕ Tambah File",
        "btn_sort": "Urutkan A-Z",
        "btn_clear": "Hapus Semua",
        "btn_support": "❤️ Dukung Developer",
        "lbl_files": "File",
        "tip_drop": "Tip: Drag & Drop file ke area ini",
        "status_ready": "Siap",
        "status_working": "Sedang memproses...",
        "status_loading_files": "Memuat file...",
        "status_done": "Selesai",
        "status_cancelled": "Dibatalkan oleh user.",
        "msg_empty": "Tidak ada file yang dipilih!",
        "msg_success": "Tugas Selesai!",
        "msg_error": "Terjadi Kesalahan",
        "msg_cancelled": "Operasi Dibatalkan",
        "msg_invalid_type": "⚠️ Beberapa file diabaikan (tipe salah).",
        "open_folder": "Buka Folder",
        "close": "Tutup",
        "cancel": "BATALKAN",
        "log_title": "Riwayat Aktivitas",
        
        "title_merge": "Gabung PDF",
        "desc_merge": "Gabungkan banyak file PDF menjadi satu.",
        "opt_clean_meta": "Hapus Metadata (Privasi)",
        "exec_merge": "EKSEKUSI PENGGABUNGAN",
        
        "title_split": "Pisah PDF",
        "desc_split": "Ambil halaman tertentu atau pecah semua.",
        "opt_split_method": "Metode Pemisahan:",
        "rb_burst": "Burst (Semua Halaman Pisah)",
        "rb_range": "Range (Halaman Tertentu)",
        "ph_range": "Contoh: 1-3, 5, 8",
        "exec_split": "EKSEKUSI PEMISAHAN",
        
        "title_comp": "Kompres PDF",
        "desc_comp": "Optimasi ukuran file & gambar.",
        "lbl_mode": "Mode Kompresi:",
        "mode_less": "Less (Ringan)",
        "mode_rec": "Recommended",
        "mode_ext": "Extreme",
        "desc_less": "Kualitas Baik. Kompresi standar (60-70%).",
        "desc_rec": "Seimbang. Kualitas oke, ukuran turun drastis.",
        "desc_ext": "BRUTAL. Hitam-Putih, Resolusi Rendah (Q=10, Max=600px).",
        "exec_comp": "MULAI KOMPRESI",
        
        "title_i2p": "Gambar ke PDF",
        "desc_i2p": "Ubah JPG/PNG menjadi PDF.",
        "sw_fit": "Sesuaikan ke A4 (Smart Rotate)",
        "exec_i2p": "KONVERSI KE PDF",
        
        "title_p2i": "PDF ke Gambar",
        "desc_p2i": "Ekstrak halaman menjadi PNG.",
        "exec_p2i": "EKSTRAK GAMBAR",
        
        "title_sec": "Keamanan PDF",
        "desc_sec": "Enkripsi atau Buka Kunci PDF.",
        "lbl_pass": "Password Dokumen:",
        "ph_pass": "Masukkan Password...",
        "btn_enc": "🔒 KUNCI (Encrypt)",
        "btn_dec": "🔓 BUKA (Decrypt)",
        
        "log_start": "Memulai proses...",
        "log_finish": "Proses selesai.",
        "log_item_success": "Sukses",
        "log_item_fail": "Gagal",
    },
    "EN": {
        "app_title": "PDF-X | Enterprise Tool",
        "sidebar_title": "PDF-X",
        "sidebar_sub": "v3.4 Ultimate",
        "nav_merge": " Merge PDF",
        "nav_split": " Split PDF",
        "nav_comp": " Compress",
        "nav_i2p": " Image to PDF",
        "nav_p2i": " PDF to Image",
        "nav_sec": " Security",
        "btn_add": "➕ Add Files",
        "btn_sort": "Sort A-Z",
        "btn_clear": "Clear All",
        "btn_support": "❤️ Support Developer",
        "lbl_files": "Files",
        "tip_drop": "Tip: Drag & Drop files here",
        "status_ready": "Ready",
        "status_working": "Processing...",
        "status_loading_files": "Loading files...",
        "status_done": "Done",
        "status_cancelled": "Cancelled by user.",
        "msg_empty": "No files selected!",
        "msg_success": "Task Completed!",
        "msg_error": "An Error Occurred",
        "msg_cancelled": "Operation Cancelled",
        "msg_invalid_type": "⚠️ Some files ignored due to invalid type.",
        "open_folder": "Open Folder",
        "close": "Close",
        "cancel": "CANCEL",
        "log_title": "Activity Log",

        "title_merge": "Merge PDF",
        "desc_merge": "Combine multiple PDFs into one.",
        "opt_clean_meta": "Clean Metadata (Privacy)",
        "exec_merge": "EXECUTE MERGE",
        
        "title_split": "Split PDF",
        "desc_split": "Extract specific pages or burst all.",
        "opt_split_method": "Split Method:",
        "rb_burst": "Burst (Separate All Pages)",
        "rb_range": "Range (Specific Pages)",
        "ph_range": "Ex: 1-3, 5, 8",
        "exec_split": "EXECUTE SPLIT",
        
        "title_comp": "Compress PDF",
        "desc_comp": "Reduce file size by optimizing images.",
        "lbl_mode": "Compression Mode:",
        "mode_less": "Less",
        "mode_rec": "Recommended",
        "mode_ext": "Extreme",
        "desc_less": "Good Quality. Standard compression (Q=60, Max=1500px).",
        "desc_rec": "Significant. Decent quality (Q=35, Max=1000px).",
        "desc_ext": "Aggressive (Max 90%). Images might be blurry.",
        "exec_comp": "START COMPRESSION",
        
        "title_i2p": "Image to PDF",
        "desc_i2p": "Convert JPG/PNG to PDF.",
        "sw_fit": "Fit to A4 Page Size (Smart Rotate)",
        "exec_i2p": "CONVERT TO PDF",
        
        "title_p2i": "PDF to Image",
        "desc_p2i": "Extract pages as PNGs.",
        "exec_p2i": "EXTRACT IMAGES",
        
        "title_sec": "PDF Security",
        "desc_sec": "Encrypt or Decrypt PDF files.",
        "lbl_pass": "Document Password:",
        "ph_pass": "Enter Password...",
        "btn_enc": "🔒 ENCRYPT",
        "btn_dec": "🔓 DECRYPT",
        
        "log_start": "Starting process...",
        "log_finish": "Process finished.",
        "log_item_success": "Success",
        "log_item_fail": "Failed",
    }
}

# --- ASET IKON (Base64) ---
# Ikon Modern Flat Design (Blue Document Style)
ICON_DATA = """
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAABMLAAATCwAAAAAA
AAAAAAAAAAAA////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALAAAACwAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAHcAAAB3AAAACwAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAACwAAAHcAAAB3AAAACwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP//AAD//wAA//8AAP//AAD/
/wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAA==
"""

# --- BACKEND LOGIC ---
class PDFProcessor:
    @staticmethod
    def get_unique_filename(directory, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(directory, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        return os.path.join(directory, new_filename)

    @staticmethod
    def merge_pdfs(file_list, output_dir, clean_meta, lang, log_cb, progress_cb, stop_event):
        try:
            log_cb(LANG[lang]["log_start"], "info")
            doc = fitz.open()
            if clean_meta: doc.set_metadata({}) 
            total = len(file_list)
            
            for idx, f in enumerate(file_list):
                if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
                try:
                    with fitz.open(f) as temp_doc:
                        doc.insert_pdf(temp_doc)
                    log_cb(f"{LANG[lang]['log_item_success']}: {os.path.basename(f)}", "success")
                except Exception as e:
                    log_cb(f"{LANG[lang]['log_item_fail']}: {os.path.basename(f)} ({str(e)})", "error")
                progress_cb((idx + 1) / total)

            if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
            
            output_path = PDFProcessor.get_unique_filename(output_dir, "PDF-X_Merged.pdf")
            doc.save(output_path, garbage=4, deflate=True)
            log_cb(f"Saved: {os.path.basename(output_path)}", "success")
            return True, output_path
        except Exception as e:
            return False, str(e)
        finally:
            if 'doc' in locals(): doc.close()
            gc.collect()

    @staticmethod
    def split_pdf(file_path, mode, range_str, output_dir, clean_meta, lang, log_cb, progress_cb, stop_event, progress_offset=0, progress_scale=1):
        try:
            log_cb(f"Opening: {os.path.basename(file_path)}", "info")
            doc = fitz.open(file_path)
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            total_pages = len(doc)

            if mode == "burst":
                for i in range(total_pages):
                    if stop_event.is_set(): return False
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    if clean_meta: new_doc.set_metadata({}) 
                    out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}_pg{i+1}.pdf")
                    new_doc.save(out_name)
                    new_doc.close()
                    
                    current_fraction = (i + 1) / total_pages
                    progress_cb(progress_offset + (current_fraction * progress_scale))
            
            elif mode == "range":
                pages = set()
                try:
                    parts = [p.strip() for p in range_str.split(',')]
                    for p in parts:
                        if '-' in p:
                            start_str, end_str = p.split('-')
                            start, end = int(start_str.strip()), int(end_str.strip())
                            pages.update(range(start-1, end))
                        else:
                            pages.add(int(p)-1)
                except ValueError:
                    raise ValueError("Format range salah")

                sorted_pages = sorted([p for p in pages if 0 <= p < total_pages])
                if not sorted_pages: raise ValueError("Halaman tidak valid")

                new_doc = fitz.open()
                for idx, p in enumerate(sorted_pages):
                    if stop_event.is_set(): return False
                    new_doc.insert_pdf(doc, from_page=p, to_page=p)
                    progress_cb(progress_offset + ((idx + 1) / len(sorted_pages) * progress_scale))
                
                if clean_meta: new_doc.set_metadata({})
                out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}_split.pdf")
                new_doc.save(out_name)
                new_doc.close()

            log_cb(f"{LANG[lang]['log_item_success']}: {os.path.basename(file_path)}", "success")
            return True
        except Exception as e:
            log_cb(f"Error {os.path.basename(file_path)}: {str(e)}", "error")
            return False
        finally:
            if 'doc' in locals(): doc.close()

    @staticmethod
    def compress_pdf(file_path, quality_level, output_dir, clean_meta, lang, log_cb, progress_cb, stop_event, progress_offset=0, progress_scale=1):
        try:
            log_cb(f"Compressing ({quality_level}): {os.path.basename(file_path)}", "info")
            doc = fitz.open(file_path)
            if clean_meta: doc.set_metadata({})
            
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            total_pages = len(doc)
            
            # AGGRESSIVE COMPRESSION SETTINGS
            SETTINGS = {
                "Less": (60, 1500, False),        
                "Recommended": (30, 900, False),
                "Extreme": (10, 600, True) 
            }
            jpeg_quality, max_width, force_grayscale = SETTINGS.get(quality_level, (30, 900, False))
            
            processed_xrefs = set()

            for page_num in range(total_pages):
                if stop_event.is_set(): return False
                
                # Clean content stream first
                try:
                    doc[page_num].clean_contents()
                except: pass

                image_list = doc[page_num].get_images()
                
                if image_list:
                    for img_info in image_list:
                        xref = img_info[0]
                        if xref in processed_xrefs: continue
                        processed_xrefs.add(xref)

                        try:
                            pix = fitz.Pixmap(doc, xref)
                            original_size = len(pix.tobytes())
                            
                            if pix.n - pix.alpha < 4: pass
                            else: pix = fitz.Pixmap(fitz.csRGB, pix)
                            
                            img_data = pix.tobytes()
                            mode = "RGB"
                            if pix.alpha:
                                temp_img = Image.frombytes("RGBA", [pix.width, pix.height], img_data)
                                background = Image.new("RGB", temp_img.size, (255, 255, 255))
                                background.paste(temp_img, mask=temp_img.split()[3]) 
                                img = background
                            else:
                                if pix.n == 1: mode = "L"
                                elif pix.n == 4: mode = "CMYK"
                                img = Image.frombytes(mode, [pix.width, pix.height], img_data)
                            
                            if force_grayscale:
                                img = img.convert("L")

                            was_modified = False
                            if img.width > max_width:
                                ratio = max_width / float(img.width)
                                new_height = int((float(img.height) * float(ratio)))
                                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                                was_modified = True
                            
                            buffer = BytesIO()
                            img.save(buffer, format="JPEG", quality=jpeg_quality, optimize=True, subsampling=0) 
                            new_data = buffer.getvalue()
                            new_size = len(new_data)
                            
                            if new_size < original_size or was_modified or force_grayscale:
                                doc.update_stream(xref, new_data)
                                doc.xref_set_key(xref, "Width", str(img.width))
                                doc.xref_set_key(xref, "Height", str(img.height))
                                doc.xref_set_key(xref, "BitsPerComponent", "8")
                                doc.xref_set_key(xref, "ColorSpace", "/DeviceGray" if img.mode == "L" else "/DeviceRGB")
                                doc.xref_set_key(xref, "Filter", "/DCTDecode")
                                doc.xref_set_key(xref, "Subtype", "/Image")
                                
                        except Exception as e:
                            continue
                            
                progress_cb(progress_offset + ((page_num + 1) / total_pages * progress_scale))

            try: doc.subset_fonts() 
            except: pass

            suffix = f"_min_{quality_level[:3].lower()}.pdf"
            out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}{suffix}")
            doc.save(out_name, garbage=4, deflate=True, clean=True)
            log_cb(f"Done: {os.path.basename(out_name)}", "success")
            return True
        except Exception as e:
            log_cb(f"Error {os.path.basename(file_path)}: {str(e)}", "error")
            return False
        finally:
            if 'doc' in locals(): doc.close()
            gc.collect()

    @staticmethod
    def images_to_pdf(file_list, output_dir, fit_a4, lang, log_cb, progress_cb, stop_event):
        try:
            doc = fitz.open()
            A4_W, A4_H = 595, 842 
            total = len(file_list)

            for idx, img_path in enumerate(file_list):
                if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
                log_cb(f"Converting: {os.path.basename(img_path)}", "info")
                try:
                    img = fitz.open(img_path)
                    rect = img[0].rect
                    pdfbytes = img.convert_to_pdf()
                    img.close()
                    imgPDF = fitz.open("pdf", pdfbytes)
                    
                    if fit_a4:
                        if rect.width > rect.height:
                            page = doc.new_page(width=A4_H, height=A4_W)
                            page.show_pdf_page(fitz.Rect(0, 0, A4_H, A4_W), imgPDF, 0)
                        else:
                            page = doc.new_page(width=A4_W, height=A4_H)
                            page.show_pdf_page(fitz.Rect(0, 0, A4_W, A4_H), imgPDF, 0)
                    else:
                        page = doc.new_page(width=rect.width, height=rect.height)
                        page.show_pdf_page(rect, imgPDF, 0)
                except Exception as e:
                    log_cb(f"Skip {os.path.basename(img_path)}: {e}", "error")
                
                progress_cb((idx + 1) / total)
            
            out_name = PDFProcessor.get_unique_filename(output_dir, "Images_Converted.pdf")
            doc.save(out_name)
            return True, out_name
        except Exception as e:
            return False, str(e)
        finally:
            if 'doc' in locals(): doc.close()

    @staticmethod
    def pdf_to_images(file_list, output_dir, lang, log_cb, progress_cb, stop_event):
        try:
            total_files = len(file_list)
            for f_idx, f in enumerate(file_list):
                if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
                doc = fitz.open(f)
                base_name = os.path.splitext(os.path.basename(f))[0]
                mat = fitz.Matrix(300 / 72, 300 / 72)
                for i in range(len(doc)):
                    if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=mat)
                    out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}_p{i+1}.png")
                    pix.save(out_name)
                progress_cb((f_idx + 1) / total_files)
                log_cb(f"Extracted: {base_name}", "success")
                doc.close()
            return True, "Selesai"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def protect_pdf(file_list, password, mode, output_dir, lang, log_cb, progress_cb, stop_event):
        try:
            total = len(file_list)
            for idx, f in enumerate(file_list):
                if stop_event.is_set(): return False, LANG[lang]["status_cancelled"]
                doc = fitz.open(f)
                base_name = os.path.splitext(os.path.basename(f))[0]
                
                if mode == "encrypt":
                    out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}_secured.pdf")
                    doc.save(out_name, encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw=password, user_pw=password)
                    log_cb(f"Encrypted: {base_name}", "success")
                else:
                    if doc.is_encrypted and not doc.authenticate(password):
                        log_cb(f"Wrong Password: {base_name}", "error")
                        doc.close()
                        continue
                    out_name = PDFProcessor.get_unique_filename(output_dir, f"{base_name}_unlocked.pdf")
                    doc.save(out_name)
                    log_cb(f"Decrypted: {base_name}", "success")
                
                doc.close()
                progress_cb((idx + 1) / total)
            return True, "Selesai"
        except Exception as e:
            return False, str(e)


# --- UI COMPONENTS ---

class ModernOverlay(ctk.CTkFrame):
    def __init__(self, master, current_lang, cancel_callback):
        super().__init__(master, fg_color="transparent")
        self.bg = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.card = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=20, border_width=2, border_color="#333")
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.45)
        self.lbl_status = ctk.CTkLabel(self.card, text=LANG[current_lang]["status_working"], font=("Arial", 28, "bold"))
        self.lbl_status.pack(pady=(40, 20))
        self.progress = ctk.CTkProgressBar(self.card, width=400, height=20, progress_color="#1f538d")
        self.progress.pack(pady=15)
        self.progress.set(0)
        self.lbl_pct = ctk.CTkLabel(self.card, text="0%", font=("Consolas", 18), text_color="#aaa")
        self.lbl_pct.pack(pady=5)
        self.btn_cancel = ctk.CTkButton(self.card, text=LANG[current_lang]["cancel"], height=45, font=FONTS["btn"],
                                        fg_color="#cf3a3a", hover_color="#8a1c1c", command=cancel_callback)
        self.btn_cancel.pack(pady=25)

    def update_progress(self, val):
        self.progress.set(val)
        self.lbl_pct.configure(text=f"{int(val*100)}%")

class LoadingOverlay(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master, fg_color="transparent")
        self.bg = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.card = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15, border_width=1, border_color="#444")
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.25)
        ctk.CTkLabel(self.card, text="⏳", font=("Arial", 48)).pack(pady=(30, 5))
        ctk.CTkLabel(self.card, text=text, font=("Arial", 18, "bold")).pack(pady=10)

class ResultModal(ctk.CTkToplevel):
    def __init__(self, master, title, message, lang, output_path=None):
        super().__init__(master)
        self.geometry("500x300")
        self.title(title)
        self.transient(master)
        self.grab_set()
        try:
            x = master.winfo_x() + (master.winfo_width()//2) - 250
            y = master.winfo_y() + (master.winfo_height()//2) - 150
            self.geometry(f"+{x}+{y}")
        except: pass
        self.resizable(False, False)
        self.config(background="#1a1a1a")
        color = "#2EA043" if "sukses" in title.lower() or "success" in title.lower() else "#cf3a3a"
        if "batal" in title.lower() or "cancel" in title.lower(): color = "#D29922"
        ctk.CTkLabel(self, text=title, font=("Arial", 24, "bold"), text_color=color).pack(pady=(25, 10))
        msg_frm = ctk.CTkFrame(self, fg_color="transparent")
        msg_frm.pack(fill="both", expand=True, padx=30)
        ctk.CTkLabel(msg_frm, text=message, wraplength=400, font=("Arial", 16)).pack(pady=10)
        btn_frm = ctk.CTkFrame(self, fg_color="transparent")
        btn_frm.pack(pady=25)
        if output_path:
            ctk.CTkButton(btn_frm, text=LANG[lang]["open_folder"], command=lambda: self.open_folder(output_path),
                          fg_color="#1f538d", width=150, height=40, font=FONTS["btn"]).pack(side="left", padx=10)
        ctk.CTkButton(btn_frm, text=LANG[lang]["close"], command=self.destroy,
                      fg_color="#444", hover_color="#333", width=120, height=40, font=FONTS["btn"]).pack(side="left", padx=10)
    def open_folder(self, path):
        try: os.startfile(path)
        except: pass
        self.destroy()

class FileQueue(ctk.CTkFrame):
    def __init__(self, master, current_lang, app_instance, file_type_filter=".pdf"):
        super().__init__(master, fg_color="transparent")
        self.files = []
        self.filter = file_type_filter
        self.lang = current_lang
        self.app = app_instance 

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", pady=(0, 5))
        self.info_lbl = ctk.CTkLabel(top_bar, text=f"0 {LANG[self.lang]['lbl_files']}", font=("Arial", 16, "bold"))
        self.info_lbl.pack(side="left", padx=5)
        self.btn_add = ctk.CTkButton(top_bar, text=LANG[self.lang]["btn_add"], width=130, height=35,
                                     font=("Arial", 14, "bold"), fg_color="#1f538d", hover_color="#14375e",
                                     command=self.browse_files)
        self.btn_add.pack(side="right", padx=5)
        self.btn_sort = ctk.CTkButton(top_bar, text=LANG[self.lang]["btn_sort"], width=100, height=35, 
                                      font=("Arial", 14), fg_color="#444", hover_color="#333",
                                      command=self.sort_files)
        self.btn_sort.pack(side="right", padx=5)
        self.list_frame = ctk.CTkScrollableFrame(self, height=220, corner_radius=10, fg_color="#212121")
        self.list_frame.pack(fill="both", expand=True, padx=0, pady=5)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=0, pady=5)
        self.btn_clear = ctk.CTkButton(btn_frame, text=LANG[self.lang]["btn_clear"], command=self.clear_all, 
                      fg_color="#cf3a3a", hover_color="#8a1c1c", width=120, height=30, font=("Arial", 14))
        self.btn_clear.pack(side="right")
        self.status_lbl = ctk.CTkLabel(self, text="", text_color="#D29922", font=("Arial", 12))
        self.status_lbl.pack(side="bottom", pady=2)

    def browse_files(self):
        filetypes = [("PDF Files", "*.pdf")] if self.filter == ".pdf" else [("All Files", "*.*")]
        if self.filter == "*": filetypes = [("Images", "*.jpg;*.jpeg;*.png;*.webp"), ("All Files", "*.*")]
        files = filedialog.askopenfilenames(title="Select Files", filetypes=filetypes)
        if files:
            self.process_files_async(files)

    def process_files_async(self, file_list):
        overlay = LoadingOverlay(self.app.main_area, LANG[self.lang]["status_loading_files"])
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        def task():
            valid_files = []
            for f in file_list:
                if not os.path.isfile(f): continue
                valid = False
                if self.filter == "*":
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp')): valid = True
                elif f.lower().endswith(self.filter):
                    valid = True
                
                if valid and f not in self.files:
                    valid_files.append(f)
            
            self.after(0, lambda: self.finish_add_files(valid_files, overlay))

        threading.Thread(target=task, daemon=True).start()

    def finish_add_files(self, new_files, overlay):
        self.files.extend(new_files)
        self.refresh_ui()
        overlay.destroy()
        if not new_files and len(self.files) == 0:
             self.show_temp_error(LANG[self.lang]["msg_invalid_type"])

    def add_file_direct(self, file_path):
        pass 

    def show_temp_error(self, msg):
        self.status_lbl.configure(text=msg)
        self.after(3000, lambda: self.status_lbl.configure(text=""))

    def remove_at(self, index):
        del self.files[index]
        self.refresh_ui()

    def sort_files(self):
        self.files.sort(key=lambda x: os.path.basename(x).lower())
        self.refresh_ui()

    def clear_all(self):
        self.files = []
        self.refresh_ui()

    def refresh_ui(self):
        for widget in self.list_frame.winfo_children(): widget.destroy()
        for idx, f in enumerate(self.files):
            size_mb = os.path.getsize(f) / (1024 * 1024)
            item = ctk.CTkFrame(self.list_frame, fg_color="#2b2b2b", corner_radius=8)
            item.pack(fill="x", padx=2, pady=4)
            icon = "📄" if f.endswith(".pdf") else "🖼️"
            ctk.CTkLabel(item, text=f"{idx+1}.", width=30, text_color="gray", font=("Arial", 14)).pack(side="left", padx=(10,0))
            ctk.CTkLabel(item, text=f"{icon}  {os.path.basename(f)}", anchor="w", font=("Arial", 15)).pack(side="left", fill="x", expand=True, padx=10)
            ctk.CTkLabel(item, text=f"{size_mb:.2f} MB", text_color="#aaa", width=80, font=("Arial", 14)).pack(side="right", padx=10)
            ctk.CTkButton(item, text="✕", width=30, height=30, fg_color="transparent", text_color="#cf3a3a",
                                    hover_color="#3a1c1c", font=("Arial", 16, "bold"), 
                                    command=lambda i=idx: self.remove_at(i)).pack(side="right", padx=(0, 5))
        self.info_lbl.configure(text=f"{len(self.files)} {LANG[self.lang]['lbl_files']}")
    
    def set_state(self, state):
        self.btn_clear.configure(state=state)
        self.btn_sort.configure(state=state)
        self.btn_add.configure(state=state)

class CompactLog(ctk.CTkScrollableFrame):
    """Log yang jauh lebih kecil dan hemat tempat"""
    def __init__(self, master, current_lang):
        super().__init__(master, height=100, fg_color="#121212", corner_radius=10, label_text=LANG[current_lang]["log_title"])
        self.configure(label_font=("Arial", 11, "bold"))

    def log(self, message, type="info"):
        def _add():
            color = "#888" # Default
            icon = "•"
            if type == "success": 
                color = "#2EA043"
                icon = "✓"
            elif type == "error": 
                color = "#cf3a3a"
                icon = "✕"
            
            # Simple Text Row
            row = ctk.CTkFrame(self, fg_color="transparent", height=20)
            row.pack(fill="x", pady=1)
            
            time_str = datetime.now().strftime("[%H:%M]")
            full_msg = f"{time_str} {icon} {message}"
            
            lbl = ctk.CTkLabel(row, text=full_msg, font=FONTS["log"], text_color=color, anchor="w")
            lbl.pack(side="left", padx=5)
            
            # Auto scroll
            self._parent_canvas.yview_moveto(1.0)
        self.after(0, _add)
        
    def update_title(self, text):
        self.configure(label_text=text)

# --- MAIN APP CLASS ---

class PDFXApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.title("PDF-X Enterprise")
        self.geometry("1200x800")
        self.current_lang = "ID" 
        try:
            icon_image = base64.b64decode(ICON_DATA)
            img = Image.open(BytesIO(icon_image))
            img.save("temp_icon.ico")
            self.iconbitmap("temp_icon.ico")
            os.remove("temp_icon.ico")
        except: pass

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        # LOG COMPACT
        self.console = CompactLog(self.main_area, self.current_lang)
        self.console.pack(side="bottom", fill="x", pady=(15, 0))

        self.nav_buttons = {}
        self.frames = {}
        self.queues = {}
        self.current_frame_name = "Merge"

        self.build_sidebar()
        self.build_modules()
        self.show_frame("Merge")
        self.update_ui_text()

    def build_sidebar(self):
        logo_frm = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frm.pack(pady=(40, 30))
        self.lbl_title = ctk.CTkLabel(logo_frm, text=LANG[self.current_lang]["sidebar_title"], font=("Impact", 40), text_color="#3B8ED0")
        self.lbl_title.pack()
        self.lbl_sub = ctk.CTkLabel(logo_frm, text=LANG[self.current_lang]["sidebar_sub"], font=("Arial", 14), text_color="#888")
        self.lbl_sub.pack()

        self.modules_keys = ["Merge", "Split", "Compress", "Img2PDF", "PDF2Img", "Security"]
        for key in self.modules_keys:
            btn = ctk.CTkButton(self.sidebar, text=key, command=lambda m=key: self.show_frame(m), 
                                fg_color="transparent", anchor="w", height=55, font=("Arial", 16, "bold"),
                                hover_color="#2c2c2c", corner_radius=0)
            btn.pack(fill="x", padx=0, pady=2)
            self.nav_buttons[key] = btn
        
        # SUPPORT BUTTON
        self.btn_support = ctk.CTkButton(self.sidebar, text=LANG[self.current_lang]["btn_support"], 
                                         command=self.open_support,
                                         fg_color="#E91E63", hover_color="#C2185B", # Pink Gumroad Style
                                         height=40, font=("Arial", 13, "bold"), corner_radius=20)
        self.btn_support.pack(side="bottom", pady=(10, 30), padx=20, fill="x")

        lang_frm = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        lang_frm.pack(side="bottom", pady=(0, 10))
        ctk.CTkLabel(lang_frm, text="Language / Bahasa:", font=("Arial", 12, "bold"), text_color="#666").pack()
        self.seg_lang = ctk.CTkSegmentedButton(lang_frm, values=["ID", "EN"], command=self.change_language, font=("Arial", 12))
        self.seg_lang.set("ID")
        self.seg_lang.pack(pady=5)

    def open_support(self):
        webbrowser.open("https://3370578580979.gumroad.com/l/PDF-X")

    def change_language(self, value):
        self.current_lang = value
        self.update_ui_text()
        self.frames = {} 
        self.queues = {}
        for widget in self.main_area.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.console:
                widget.destroy()
            if widget == self.console:
                self.console.update_title(LANG[self.current_lang]["log_title"])
        
        self.build_modules()
        self.show_frame(self.current_frame_name)

    def update_ui_text(self):
        self.title(LANG[self.current_lang]["app_title"])
        self.lbl_title.configure(text=LANG[self.current_lang]["sidebar_title"])
        self.lbl_sub.configure(text=LANG[self.current_lang]["sidebar_sub"])
        
        # Update Nav Buttons
        nav_map = {
            "Merge": "nav_merge", "Split": "nav_split", "Compress": "nav_comp",
            "Img2PDF": "nav_i2p", "PDF2Img": "nav_p2i", "Security": "nav_sec"
        }
        for key, text_key in nav_map.items():
            self.nav_buttons[key].configure(text=LANG[self.current_lang][text_key])
            
        # Update Support Button
        self.btn_support.configure(text=LANG[self.current_lang]["btn_support"])

    def build_modules(self):
        self.create_module("Merge", "title_merge", "desc_merge", ".pdf", "exec_merge", self.logic_merge, self.opt_merge)
        self.create_module("Split", "title_split", "desc_split", ".pdf", "exec_split", self.logic_split, self.opt_split)
        self.create_module("Compress", "title_comp", "desc_comp", ".pdf", "exec_comp", self.logic_compress, self.opt_comp)
        self.create_module("Img2PDF", "title_i2p", "desc_i2p", "*", "exec_i2p", self.logic_img2pdf, self.opt_i2p)
        self.create_module("PDF2Img", "title_p2i", "desc_p2i", ".pdf", "exec_p2i", self.logic_pdf2img)
        self.create_security_module()

    def create_module(self, key, title_k, desc_k, f_type, btn_k, logic_cmd, opts_widget=None):
        f = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.frames[key] = f
        head = ctk.CTkFrame(f, fg_color="transparent")
        head.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(head, text=LANG[self.current_lang][title_k], font=FONTS["h1"]).pack(anchor="w")
        ctk.CTkLabel(head, text=LANG[self.current_lang][desc_k], font=FONTS["body_small"], text_color="gray").pack(anchor="w")
        q = FileQueue(f, self.current_lang, self, f_type) 
        q.pack(fill="x", expand=False, pady=15)
        self.queues[key] = q
        dz = ctk.CTkLabel(f, text=LANG[self.current_lang]["tip_drop"], text_color="#666", font=("Arial", 13))
        dz.pack(fill="x", pady=(0, 15))
        dz.drop_target_register(DND_FILES)
        dz.dnd_bind('<<Drop>>', lambda e: self.on_drop(e, q))
        if opts_widget: opts_widget(f)
        btn = ctk.CTkButton(f, text=LANG[self.current_lang][btn_k], height=60, font=FONTS["btn"], 
                            command=lambda: self.run_async(logic_cmd, q),
                            fg_color="#2EA043", hover_color="#238636")
        btn.pack(fill="x", pady=25)

    def create_security_module(self):
        f = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.frames["Security"] = f
        head = ctk.CTkFrame(f, fg_color="transparent")
        head.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(head, text=LANG[self.current_lang]["title_sec"], font=FONTS["h1"]).pack(anchor="w")
        ctk.CTkLabel(head, text=LANG[self.current_lang]["desc_sec"], font=FONTS["body_small"], text_color="gray").pack(anchor="w")
        q = FileQueue(f, self.current_lang, self, ".pdf")
        q.pack(fill="x", expand=False, pady=15)
        self.queues["Security"] = q
        dz = ctk.CTkLabel(f, text=LANG[self.current_lang]["tip_drop"], text_color="#666", font=("Arial", 13))
        dz.pack(fill="x", pady=(0, 15))
        dz.drop_target_register(DND_FILES)
        dz.dnd_bind('<<Drop>>', lambda e: self.on_drop(e, q))
        sec_opts = ctk.CTkFrame(f, fg_color="#252525", corner_radius=10)
        sec_opts.pack(fill="x", pady=5, ipady=15)
        ctk.CTkLabel(sec_opts, text=LANG[self.current_lang]["lbl_pass"], font=FONTS["h3"]).pack(anchor="w", padx=20, pady=(10,5))
        self.sec_pass = ctk.CTkEntry(sec_opts, placeholder_text=LANG[self.current_lang]["ph_pass"], show="*", width=350, height=40, font=("Arial", 14))
        self.sec_pass.pack(fill="x", padx=20, pady=10)
        btn_grid = ctk.CTkFrame(f, fg_color="transparent")
        btn_grid.pack(fill="x", pady=25)
        
        ctk.CTkButton(btn_grid, text=LANG[self.current_lang]["btn_enc"], fg_color="#D29922", text_color="black", hover_color="#ac7b15", 
                      height=60, font=FONTS["btn"],
                      command=lambda: self.run_async(lambda f, od, lang, l, p, stop: self.logic_security(f, od, lang, l, p, stop, "encrypt"), q)).pack(side="left", fill="x", expand=True, padx=(0,10))
        
        ctk.CTkButton(btn_grid, text=LANG[self.current_lang]["btn_dec"], fg_color="#238636", text_color="white", hover_color="#1a6328",
                      height=60, font=FONTS["btn"],
                      command=lambda: self.run_async(lambda f, od, lang, l, p, stop: self.logic_security(f, od, lang, l, p, stop, "decrypt"), q)).pack(side="right", fill="x", expand=True, padx=(10,0))

    def opt_merge(self, parent):
        opt = ctk.CTkFrame(parent, fg_color="transparent")
        opt.pack(fill="x", pady=10)
        self.merge_clean = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(opt, text=LANG[self.current_lang]["opt_clean_meta"], variable=self.merge_clean, font=FONTS["body"]).pack(anchor="w", padx=10)

    def opt_split(self, parent):
        opt = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        opt.pack(fill="x", pady=15, padx=5, ipady=10)
        self.split_mode = ctk.StringVar(value="burst")
        self.split_clean = ctk.BooleanVar(value=False)
        ctk.CTkLabel(opt, text=LANG[self.current_lang]["opt_split_method"], font=FONTS["h3"]).pack(anchor="w", padx=20, pady=10)
        ctk.CTkRadioButton(opt, text=LANG[self.current_lang]["rb_burst"], variable=self.split_mode, value="burst", font=FONTS["body"]).pack(anchor="w", padx=20, pady=5)
        ctk.CTkRadioButton(opt, text=LANG[self.current_lang]["rb_range"], variable=self.split_mode, value="range", font=FONTS["body"]).pack(anchor="w", padx=20, pady=5)
        self.split_range = ctk.CTkEntry(opt, placeholder_text=LANG[self.current_lang]["ph_range"], width=350, height=35, font=("Arial", 14))
        self.split_range.pack(anchor="w", padx=45, pady=(5,15))
        ctk.CTkSwitch(opt, text=LANG[self.current_lang]["opt_clean_meta"], variable=self.split_clean, font=FONTS["body"]).pack(anchor="w", padx=20, pady=5)

    def opt_comp(self, parent):
        sl_frame = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        sl_frame.pack(fill="x", pady=15, ipady=10)
        self.comp_clean = ctk.BooleanVar(value=False)
        
        # New Segmented Button Logic
        self.comp_mode = ctk.StringVar(value="Recommended")
        
        ctk.CTkLabel(sl_frame, text=LANG[self.current_lang]["lbl_mode"], font=FONTS["h3"]).pack(anchor="w", padx=20, pady=(10,5))
        
        modes = [LANG[self.current_lang]["mode_less"], LANG[self.current_lang]["mode_rec"], LANG[self.current_lang]["mode_ext"]]
        # Map localized labels back to internal keys for logic if needed, or simple index
        # Let's map display values to internal keys
        self.mode_map = {
            LANG[self.current_lang]["mode_less"]: "Less",
            LANG[self.current_lang]["mode_rec"]: "Recommended",
            LANG[self.current_lang]["mode_ext"]: "Extreme"
        }
        
        seg = ctk.CTkSegmentedButton(sl_frame, values=modes, variable=self.comp_mode, command=self.update_comp_desc, font=("Arial", 13, "bold"), height=40)
        seg.pack(fill="x", padx=20, pady=5)
        seg.set(LANG[self.current_lang]["mode_rec"]) # Default
        
        self.comp_desc_lbl = ctk.CTkLabel(sl_frame, text=LANG[self.current_lang]["desc_rec"], font=("Arial", 12), text_color="#aaa", wraplength=500, justify="left")
        self.comp_desc_lbl.pack(anchor="w", padx=20, pady=(5, 15))
        
        ctk.CTkSwitch(sl_frame, text=LANG[self.current_lang]["opt_clean_meta"], variable=self.comp_clean, font=FONTS["body"]).pack(anchor="w", padx=20, pady=5)

    def update_comp_desc(self, value):
        key = self.mode_map.get(value, "Recommended")
        desc_map = {
            "Less": "desc_less",
            "Recommended": "desc_rec",
            "Extreme": "desc_ext"
        }
        self.comp_desc_lbl.configure(text=LANG[self.current_lang][desc_map[key]])

    def opt_i2p(self, parent):
        opt = ctk.CTkFrame(parent, fg_color="transparent")
        opt.pack(fill="x", pady=10)
        self.img_fit = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(opt, text=LANG[self.current_lang]["sw_fit"], variable=self.img_fit, font=FONTS["body"]).pack(anchor="w", padx=10)

    def on_drop(self, event, queue_widget):
        files = self.tk.splitlist(event.data)
        if files:
            queue_widget.process_files_async(files)

    def show_frame(self, name):
        self.current_frame_name = name
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name: btn.configure(fg_color="#1f538d", text_color="white")
            else: btn.configure(fg_color="transparent", text_color="#ccc")
        for f in self.frames.values(): f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def run_async(self, func, queue_widget):
        files = queue_widget.files
        if not files:
            ResultModal(self, LANG[self.current_lang]["msg_error"], LANG[self.current_lang]["msg_empty"], self.current_lang)
            return
        
        out_dir = filedialog.askdirectory(title=LANG[self.current_lang]["open_folder"])
        if not out_dir: return

        self.stop_event = threading.Event()
        
        self.overlay = ModernOverlay(self.main_area, self.current_lang, cancel_callback=self.cancel_operation)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.console.log("--- START ---", "info")
        
        def thread_task():
            try:
                success, msg = func(files, out_dir, self.current_lang, self.console.log, self.overlay.update_progress, self.stop_event)
                
                if self.stop_event.is_set():
                    self.after(0, lambda: ResultModal(self, LANG[self.current_lang]["msg_cancelled"], LANG[self.current_lang]["status_cancelled"], self.current_lang))
                elif success:
                    self.after(0, lambda: ResultModal(self, LANG[self.current_lang]["msg_success"], msg, self.current_lang, out_dir))
                else:
                    self.after(0, lambda: ResultModal(self, LANG[self.current_lang]["msg_error"], msg, self.current_lang))
            except Exception as e:
                self.after(0, lambda: ResultModal(self, LANG[self.current_lang]["msg_error"], str(e), self.current_lang))
            finally:
                self.after(0, lambda: self.overlay.destroy())

        self.worker_thread = threading.Thread(target=thread_task, daemon=True)
        self.worker_thread.start()

    def cancel_operation(self):
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
            self.console.log("CANCELLING...", "error")

    # --- WRAPPERS ---
    def logic_merge(self, f, od, lang, l, p, stop): 
        return PDFProcessor.merge_pdfs(f, od, self.merge_clean.get(), lang, l, p, stop)
    
    def logic_split(self, f, od, lang, l, p, stop):
        mode, rng = self.split_mode.get(), self.split_range.get()
        total = len(f)
        clean = self.split_clean.get()
        for i, file in enumerate(f):
            if stop.is_set(): return False, LANG[lang]["status_cancelled"]
            PDFProcessor.split_pdf(file, mode, rng, od, clean, lang, l, p, stop, progress_offset=i/total, progress_scale=1/total)
        return True, "Batch Split Completed"

    def logic_compress(self, f, od, lang, l, p, stop):
        # Get raw label value
        raw_val = self.comp_mode.get()
        # Convert back to internal key "Less", "Recommended", "Extreme"
        internal_key = "Recommended" # Default
        for k, v in self.mode_map.items():
            if k == raw_val:
                internal_key = v
                break
        
        clean = self.comp_clean.get()
        total = len(f)
        for i, file in enumerate(f):
            if stop.is_set(): return False, LANG[lang]["status_cancelled"]
            # Pass string key (e.g., "Extreme") to processor
            PDFProcessor.compress_pdf(file, internal_key, od, clean, lang, l, p, stop, progress_offset=i/total, progress_scale=1/total)
        return True, "Batch Compress Completed"
        
    def logic_img2pdf(self, f, od, lang, l, p, stop): 
        return PDFProcessor.images_to_pdf(f, od, self.img_fit.get(), lang, l, p, stop)
        
    def logic_pdf2img(self, f, od, lang, l, p, stop): 
        return PDFProcessor.pdf_to_images(f, od, lang, l, p, stop)
        
    def logic_security(self, f, od, lang, l, p, stop, mode):
        pw = self.sec_pass.get()
        if not pw: raise ValueError("Password Required")
        return PDFProcessor.protect_pdf(f, pw, mode, od, lang, l, p, stop)

if __name__ == "__main__":
    app = PDFXApp()
    app.mainloop()