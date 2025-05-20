import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def veritabani_baglantisi():
    conn = sqlite3.connect("veteriner.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS kullanicilar (id INTEGER PRIMARY KEY, kullaniciadi TEXT, sifre TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS hayvanlar (id INTEGER PRIMARY KEY, ad TEXT, tur TEXT, cins TEXT, cinsiyet TEXT, asi TEXT, tarih TEXT)"
    )
    conn.commit()
    return conn, cursor


def ekle():
    yeni_kullanici = yenikullaniciadi_entry.get()
    yeni_sifre = yenisifre_entry.get()

    if not yeni_kullanici or not yeni_sifre:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurunuz!")
        return

    conn, cursor = veritabani_baglantisi()
    cursor.execute("INSERT INTO kullanicilar (kullaniciadi, sifre) VALUES (?, ?)", (yeni_kullanici, yeni_sifre))
    conn.commit()
    conn.close()

    messagebox.showinfo("İşlem Başarılı", "Kullanıcı başarılı bir şekilde eklenmiştir.")


def giris():
    kullaniciadi = kullaniciadi_entry.get()
    sifre = sifre_entry.get()

    conn, cursor = veritabani_baglantisi()
    cursor.execute("SELECT * FROM kullanicilar WHERE kullaniciadi = ? AND sifre = ?", (kullaniciadi, sifre))
    kullanici = cursor.fetchone()
    conn.close()

    if kullanici:
        messagebox.showinfo("Başarılı", "Giriş başarılı! Hoş geldiniz, Veteriner.")
        hayvan_kayit_ekrani()
    else:
        messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre. Lütfen tekrar deneyin.")


def ana_menu():
    global yenikullaniciadi_entry, yenisifre_entry, ana_pencere

    ana_pencere = tk.Toplevel()
    ana_pencere.title("Yeni Kullanıcı Ekleme")
    ana_pencere.geometry("300x200")

    tk.Label(ana_pencere, text="Yeni Kullanıcı Adı:").pack(pady=5)
    yenikullaniciadi_entry = tk.Entry(ana_pencere)
    yenikullaniciadi_entry.pack(pady=5)

    tk.Label(ana_pencere, text="Yeni Şifre:").pack(pady=5)
    yenisifre_entry = tk.Entry(ana_pencere, show="*")
    yenisifre_entry.pack(pady=5)

    tk.Button(ana_pencere, text="Ekle", command=ekle).pack(pady=5)


def tur_secildi(event):
    tur = combo_tur.get()
    combo_cins['values'] = []
    if tur == "Kedi":
        combo_cins['values'] = ["Tekir", "British", "Scottish", "Van Kedisi", "Siyam"]
    elif tur == "Köpek":
        combo_cins['values'] = ["Golden", "Bulldog", "Labrador", "Chihuahua"]
    elif tur == "Kuş":
        combo_cins['values'] = ["Muhabbet Kuşu", "Papağan", "Kanarya"]


def verileri_goster():
    conn, cursor = veritabani_baglantisi()
    cursor.execute("SELECT * FROM hayvanlar")
    hayvanlar = cursor.fetchall()
    conn.close()

    for hayvan in hayvanlar:

        liste_veriler.insert(tk.END,
                             f"{hayvan[1]} - {hayvan[2]} - {hayvan[3]} - {hayvan[4]} - {hayvan[5]} - {hayvan[6]}")


def hayvan_kayit_ekrani():
    pencere = tk.Toplevel()
    pencere.title("Hayvan Kayıt Ekranı")
    pencere.geometry("500x600")
    pencere.minsize(500, 700)
    pencere.maxsize(500, 700)
    pencere.configure(bg="#f0f8ff")

    baslik = tk.Label(pencere, text="Hayvan Kayıt Ekranı", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="purple")
    baslik.pack(pady=10)

    global entry_ad, combo_tur, combo_cins, combo_cinsiyet, entry_asi, entry_tarih, liste_veriler

    label_ad = tk.Label(pencere, text="Hayvan Adı:", font=("Arial", 12), bg="#f0f8ff")
    label_ad.pack(pady=5)
    entry_ad = tk.Entry(pencere, font=("Arial", 12))
    entry_ad.pack(pady=5)

    label_tur = tk.Label(pencere, text="Hayvan Türü:", font=("Arial", 12), bg="#f0f8ff")
    label_tur.pack(pady=5)
    combo_tur = ttk.Combobox(pencere, values=["Kedi", "Köpek", "Kuş"], font=("Arial", 12), state="readonly")
    combo_tur.pack(pady=5)
    combo_tur.bind("<<ComboboxSelected>>", tur_secildi)

    label_cins = tk.Label(pencere, text="Hayvan Cinsi:", font=("Arial", 12), bg="#f0f8ff")
    label_cins.pack(pady=5)
    combo_cins = ttk.Combobox(pencere, font=("Arial", 12), state="readonly")
    combo_cins.pack(pady=5)

    label_cinsiyet = tk.Label(pencere, text="Cinsiyet:", font=("Arial", 12), bg="#f0f8ff")
    label_cinsiyet.pack(pady=5)
    combo_cinsiyet = ttk.Combobox(pencere, values=["Dişi", "Erkek"], font=("Arial", 12), state="readonly")
    combo_cinsiyet.pack(pady=5)

    label_asi = tk.Label(pencere, text="Aşı Bilgisi:", font=("Arial", 12), bg="#f0f8ff")
    label_asi.pack(pady=5)
    entry_asi = tk.Entry(pencere, font=("Arial", 12))
    entry_asi.pack(pady=5)

    label_tarih = tk.Label(pencere, text="Aşı Tarihi:", font=("Arial", 12), bg="#f0f8ff")
    label_tarih.pack(pady=5)
    entry_tarih = tk.Entry(pencere, font=("Arial", 12))
    entry_tarih.pack(pady=5)

    def kaydet():
        ad = entry_ad.get()
        tur = combo_tur.get()
        cins = combo_cins.get()
        cinsiyet = combo_cinsiyet.get()
        asi = entry_asi.get()
        tarih = entry_tarih.get()

        if not ad or not tur or not cins or not cinsiyet or not asi or not tarih:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurunuz!")
            return

        conn, cursor = veritabani_baglantisi()
        cursor.execute("INSERT INTO hayvanlar (ad, tur, cins, cinsiyet, asi, tarih) VALUES (?, ?, ?, ?, ?, ?)",
                       (ad, tur, cins, cinsiyet, asi, tarih))
        conn.commit()
        conn.close()

        messagebox.showinfo("İşlem Başarılı", f"{ad} adlı hayvan başarıyla kaydedildi.")

        verileri_goster()

        entry_ad.delete(0, tk.END)
        entry_asi.delete(0, tk.END)
        entry_tarih.delete(0, tk.END)

    buton_kaydet = tk.Button(pencere, text="Kaydet", font=("Arial", 12, "bold"), bg="#32cd32", fg="white",
                             command=kaydet)
    buton_kaydet.pack(pady=10)

    label_veriler = tk.Label(pencere, text="Kayıtlı Hayvanlar:", font=("Arial", 12), bg="#f0f8ff")
    label_veriler.pack(pady=5)
    liste_veriler = tk.Listbox(pencere, font=("Arial", 12), width=50, height=10)
    liste_veriler.pack(pady=5)


def giris_ekrani_olustur():
    global kullaniciadi_entry, sifre_entry

    root = tk.Tk()
    root.title("Veteriner Giriş Ekranı")
    root.geometry("400x300")
    baslik = tk.Label(root, text="Veteriner Sistemi", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="purple")
    baslik.pack(pady=10)
    root.minsize(400, 300)
    root.maxsize(400, 300)
    tk.Label(root, text="Kullanıcı Adı:").pack(pady=5)
    kullaniciadi_entry = tk.Entry(root)
    kullaniciadi_entry.pack(pady=5)

    tk.Label(root, text="Şifre:").pack(pady=5)
    sifre_entry = tk.Entry(root, show="*")
    sifre_entry.pack(pady=5)

    tk.Button(root, text="Giriş Yap", command=giris).pack(pady=10)
    tk.Button(root, text="Yeni Kullanıcı Ekle", command=ana_menu).pack(pady=5)
    root.mainloop()



if __name__ == "__main__":
    giris_ekrani_olustur()
