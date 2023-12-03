import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox
import pickle

# ------------------------- Variable dan Window Root TKinter ------------------------------------

barang_dibeli = []
iid_pembelian = 0
iid_barang = 0
iid_jendela_edit = 0
id_barang_dirubah = 0
total = 0

#------------------------ Fungsi dalam Aplikasi --------------------------------------------------
def validate_entry(value):
    if not value:
        messagebox.showwarning("Warning", "Isikan Jumlah")
        return False
    return True

def fungsi_tambah():
    if validate_entry(jumlah_entry.get()):
        tambah_pembelian()
    
def fungsi_hapus():
    selectedItem = tabel_pembelian.selection()[0]
    id_barang = tabel_pembelian.item(selectedItem)['values'][0]
    tabel_pembelian.delete(selectedItem)
 
    for x in barang_dibeli:
        if x[0] == id_barang:
            barang_dibeli.remove(x)
        
    update_total()

def fungsi_checkout():
    global barang_dibeli
    global total
    for x in barang_dibeli:
        for i in daftar_barang():
            if i[0] == x[0]:
                print(i)
    uang_pelanggan = uang_pelanggan_entry.get()
    kembalian = int(uang_pelanggan) - total
    kembalian_entry.delete(0, "end")
    kembalian_entry.insert(0, str(kembalian))

def update_total():
    global barang_dibeli
    global total
    total = 0
    for x in barang_dibeli:
        total += int(x[1]) * int(x[2])
    print(total)
    total_entry.delete(0, "end")
    total_entry.insert(0, str(total))
    
def tambah_pembelian():
    global iid_pembelian
    daftar = daftar_barang()
    nama = name_entry.get()
    jumlah = jumlah_entry.get()
    for x in daftar:
        if x[0] == 0 or x[1] == nama:
            harga = (x[2] * int(jumlah))
            tabel_pembelian.insert(parent='', index='end', iid = iid_pembelian , text='', values=(x[0], x[1], jumlah, harga))
            iid_pembelian += 1
            barang_dibeli.append([x[0], x[2], jumlah])
            update_total()
            break

def fungsi_clear():
    global iid_pembelian
    global total
    name_entry.delete(0, "end")
    jumlah_entry.delete(0, "end")
    total_entry.delete(0, "end")
    uang_pelanggan_entry.delete(0, "end")
    kembalian_entry.delete(0, "end")
    total_entry.insert(0, "0")

    for x in range(0, iid_pembelian):
        tabel_pembelian.delete(x)
    iid_pembelian = 0
    total = 0
    

#--------------------------- SQL -----------------------------------------------
conn = sqlite3.connect("data.db")
cur = conn.cursor()

def tambah_database_barang():
    cur.execute("""CREATE TABLE IF NOT EXISTS barang (
                id  INT PRIMARY KEY NOT NUll,
                nama    TEXT    NOT NULL,
                jumlah  INT     NOT NULL,
                harga   INT     NOT NULL
    )""")
    conn.commit()

def daftar_barang():
    cur.execute("SELECT * FROM barang")
    return cur.fetchall()

def get_last_id():
    cur.execute("SELECT * FROM barang ORDER BY id DESC LIMIT 1")
    return cur.fetchone()[0]

# --------------  Edit Database ----------------------------------------------

def jendela_tambah_barang():
    global conn
    global cur
    def tambah_barang(id, nama, jumlah, harga):
        cur.execute("INSERT INTO barang VALUES (?, ?, ?, ?)", (id, nama, jumlah, harga))
        conn.commit()

    def hapus_barang(id):
        cur.execute("DELETE FROM barang WHERE id=?", (id,))
        print("Pengahpusan Suksess")
        conn.commit()

    def daftar_barang():
        cur.execute("SELECT * FROM barang")
        return cur.fetchall()

    def ubah_barang(id, nama, jumlah, harga):
        cur.execute("UPDATE barang SET nama = ?, jumlah = ?, harga = ? WHERE id = ?", (nama, jumlah, harga, id))

    def hapus_daftar_barang(a):
        global iid_jendela_edit
        try:
            for x in range(0, iid_jendela_edit):
                tabel_pencarian.delete(x)
            iid_jendela_edit = 0
        except tk.TclError :
            iid_jendela_edit = 0
            print("Daftar Kosong")

    def refresh_daftar_barang():
        global iid_jendela_edit
        hapus_daftar_barang(1)
        for x in daftar_barang():
            tabel_pencarian.insert(parent='', index='end', iid=iid_jendela_edit, text='', values=(x[0], x[1], x[2], x[3]))
            iid_jendela_edit += 1
    
    def fungsi_tambah():
        global iid_jendela_edit
        try:
            iid_jendela_edit = get_last_id()
        except TypeError:
            iid_jendela_edit = 0

        iid_jendela_edit += 1
        id = iid_jendela_edit
        nama = name_entry_database.get()
        jumlah = jumlah_entry_database.get()
        harga = harga_entry_database.get()
        tambah_barang(id, nama, jumlah, harga)
        refresh_daftar_barang()

    def fungsi_hapus():
        selectedItem = tabel_pencarian.selection()[0]
        id = tabel_pencarian.item(selectedItem)['values'][0]
        print(id)
        hapus_barang(id)
        refresh_daftar_barang()

    def fungsi_ubah():
        global id_barang_dirubah
        id_barang = id_barang_dirubah
        nama = name_entry_database.get()
        jumlah = jumlah_entry_database.get()
        harga = harga_entry_database.get()
        ubah_barang(id_barang, nama, jumlah, harga)
        refresh_daftar_barang()


    win = tk.Tk()
    win.title("Edit data daftar barang")

    frame_entry = tk.Frame(win)
    frame_daftar_barang = tk.Frame(win)
    frame_entry.grid(row=0, column=0)
    frame_daftar_barang.grid(row=0, column=1)


    name_label_database = tk.Label(frame_entry, text="Nama Barang", width=45)
    name_entry_database = tk.Entry(frame_entry, width=45)

    jumlah_label_database = tk.Label(frame_entry, text="Jumlah", width=45)
    jumlah_entry_database = tk.Entry(frame_entry, width=45)

    harga_label_database = tk.Label(frame_entry, text="Harga", width=45)
    harga_entry_database = tk.Entry(frame_entry, width=45)

    tambah_button = tk.Button(frame_entry, text="Tambah", command=fungsi_tambah)
    kurang_button = tk.Button(frame_entry, text="Hapus", command=fungsi_hapus)
    hapus_button = tk.Button(frame_entry, text="Ubah", command=fungsi_ubah)

    name_label_database.grid(row=0, column=0, columnspan=3)
    name_entry_database.grid(row=1, column=0, columnspan=3)

    jumlah_label_database.grid(row=2, column=0, columnspan=3)
    jumlah_entry_database.grid(row=3, column=0, columnspan=3)

    harga_label_database.grid(row=4, column=0, columnspan=3)
    harga_entry_database.grid(row=5, column=0, columnspan=3)

    tambah_button.grid(row=6, column=0, pady=10)
    kurang_button.grid(row=6, column=1, pady=10)
    hapus_button.grid(row=6, column=2, pady=10)

    # -------------- Tabel Pencarian / Daftar barang -----------------------------------------
    # Bar Pencarian
    pencarian_entry = tk.Entry(frame_daftar_barang)
    pencarian_entry.insert(0, "Cari")

    # Tabel
    tabel_pencarian = ttk.Treeview(frame_daftar_barang)

    tabel_pencarian['columns'] = ('id', 'nama barang', 'jumlah', 'harga')

    tabel_pencarian.column("#0", width=0,  stretch="no")
    tabel_pencarian.column("id",anchor="center", width=80)
    tabel_pencarian.column("nama barang",anchor="center",width=80)
    tabel_pencarian.column("jumlah",anchor="center",width=80)
    tabel_pencarian.column("harga",anchor="center",width=80)

    tabel_pencarian.heading("#0",text="",anchor="center")
    tabel_pencarian.heading("id",text="ID",anchor="center")
    tabel_pencarian.heading("nama barang",text="Nama",anchor="center")
    tabel_pencarian.heading("jumlah",text="Jumlah",anchor="center")
    tabel_pencarian.heading("harga",text="Harga",anchor="center")

    tombol_pencarian = tk.Button(frame_daftar_barang, text="Cari", command=lambda:fungsi_search(pencarian_entry.get()), padx=10)

    pencarian_entry.grid(row=0, column=0, pady=10)
    tombol_pencarian.grid(row=0, column=1)
    tabel_pencarian.grid(row=1, column=0, columnspan=2 , pady=30)

    def displaySelectedItem(a):

        global id_barang_dirubah
        # Bersihkan Entry (Hapus isi nama, uang pelanggan, kembalian)
        name_entry_database.delete(0, "end")
        jumlah_entry_database.delete(0,"end")
        harga_entry_database.delete(0,"end")

        selectedItem = tabel_pencarian.selection()[0]
        name_entry_database.insert(0, tabel_pencarian.item(selectedItem)['values'][1])
        jumlah_entry_database.insert(0, tabel_pencarian.item(selectedItem)['values'][2])
        harga_entry_database.insert(0, tabel_pencarian.item(selectedItem)['values'][3])
        id_barang_dirubah = tabel_pencarian.item(selectedItem)['values'][0]

    def fungsi_search(barang):
        global iid_jendela_edit
        hapus_daftar_barang(1)
        for x in daftar_barang():
            if barang.lower() in x[1].lower():
                tabel_pencarian.insert(parent='', index='end', iid = iid_jendela_edit, text='', values=(x[0], x[1], x[2], x[3]))
                iid_jendela_edit += 1

    tabel_pencarian.bind("<<TreeviewSelect>>", displaySelectedItem) #Menghubungkan tabel pencarian dengan fungsi displaySelectedItem()

    refresh_daftar_barang()
    win.mainloop()

# -------------------------- Tambah Database Barang ------------------------------------------------

tambah_database_barang()

# -------------------------- Window Root TKINTER ------------------------------------------------
root = tk.Tk()
root.geometry("800x600")
root.title("Kasir")

frame_entry = tk.Frame(root, pady=25, padx=25)
frame_daftar_barang = tk.Frame(root, pady=25, padx=25)
frame_pembelian = tk.Frame(root)

frame_entry.grid(row=0, column=0)
frame_daftar_barang.grid(row=0, column=1)
frame_pembelian.grid(row=1, column=0, columnspan=2)

# -------------------------- Entry Kasir ------------------------------------------------
name_label = tk.Label(frame_entry, text="Nama Barang", width=45)
name_entry = tk.Entry(frame_entry, width=45)

jumlah_label = tk.Label(frame_entry, text="Jumlah", width=45)
jumlah_entry = tk.Entry(frame_entry, width=45)

total_label = tk.Label(frame_entry, text="Total", width=45)
total_entry = tk.Entry(frame_entry, width=45)
total_entry.insert(0, 0)

uang_pelanggan_label = tk.Label(frame_entry, text="Uang Pelanggan", width=45)
uang_pelanggan_entry = tk.Entry(frame_entry, width=45)

kembalian_label = tk.Label(frame_entry, text="Kembalian", width=45)
kembalian_entry = tk.Entry(frame_entry, width=45)

label_insert = tk.Label(frame_entry, text=" ")

tambah_button = tk.Button(frame_entry, text="Tambah", command=fungsi_tambah)
hapus_button = tk.Button(frame_entry, text="Hapus", command=fungsi_hapus)
checkout_button = tk.Button(frame_entry, text="Checkout", command=fungsi_checkout)
clear_button = tk.Button(frame_entry, text="Clear", command=fungsi_clear)


# ------------------ Entry Grid -------------------------------------------------

name_label.grid(row=0, column=0, columnspan=4)
name_entry.grid(row=1, column=0, columnspan=4)

jumlah_label.grid(row=2, column=0, columnspan=4)
jumlah_entry.grid(row=3, column=0, columnspan=4)

total_label.grid(row=4, column=0, columnspan=4)
total_entry.grid(row=5, column=0, columnspan=4)

uang_pelanggan_label.grid(row=6, column=0, columnspan=4)
uang_pelanggan_entry.grid(row=7, column=0, columnspan=4)

kembalian_label.grid(row=8, column=0, columnspan=4)
kembalian_entry.grid(row=9, column=0, columnspan=4)

label_insert.grid(row=10, column=0, columnspan=4)

tambah_button.grid(row=11, column=0)
hapus_button.grid(row=11, column=1)
checkout_button.grid(row=11, column=2)
clear_button.grid(row=11, column=3)

# -------------- Tabel Pencarian / Daftar barang -----------------------------------------

# Tabel
tabel_pencarian = ttk.Treeview(frame_daftar_barang)

tabel_pencarian['columns'] = ('id', 'nama barang', 'jumlah', 'harga')

tabel_pencarian.column("#0", width=0,  stretch="no")
tabel_pencarian.column("id",anchor="center", width=80)
tabel_pencarian.column("nama barang",anchor="center",width=80)
tabel_pencarian.column("jumlah",anchor="center",width=80)
tabel_pencarian.column("harga",anchor="center",width=80)

tabel_pencarian.heading("#0",text="",anchor="center")
tabel_pencarian.heading("id",text="ID",anchor="center")
tabel_pencarian.heading("nama barang",text="Nama",anchor="center")
tabel_pencarian.heading("jumlah",text="Jumlah",anchor="center")
tabel_pencarian.heading("harga",text="Harga",anchor="center")

def hapus_daftar_barang():
    global iid_barang
    for x in range(0, iid_barang):
        tabel_pencarian.delete(x)
    iid_barang = 0

def refresh_daftar_barang():
    global iid_barang
    hapus_daftar_barang()
    for x in daftar_barang():
        tabel_pencarian.insert(parent='', index='end', iid = iid_barang, text='', values=(x[0], x[1], x[2], x[3]))
        iid_barang += 1

def fungsi_search(barang):
    global iid_barang
    hapus_daftar_barang()
    for x in daftar_barang():
        print(barang, x)
        if barang.lower() in x[1].lower():
            tabel_pencarian.insert(parent='', index='end', iid = iid_barang, text='', values=(x[0], x[1], x[2], x[3]))
            iid_barang += 1
            print(x)

refresh_daftar_barang()

# Bar Pencarian
pencarian_entry = tk.Entry(frame_daftar_barang)
pencarian_entry.insert(0, "")

tombol_pencarian = tk.Button(frame_daftar_barang, text="Cari", command=lambda:fungsi_search(pencarian_entry.get()), padx=10)

tombol_edit_database = tk.Button(frame_daftar_barang, text="Edit Database", command=jendela_tambah_barang)
tombol_refresh_database = tk.Button(frame_daftar_barang, text="Refresh Database", command=refresh_daftar_barang)

label_insert2 = tk.Label(frame_daftar_barang, text=" ")

pencarian_entry.grid(row=0, column=0)
tombol_pencarian.grid(row=0, column=1)
tabel_pencarian.grid(row=1, column=0, columnspan=2)

label_insert2.grid(row=2, column=0, columnspan=2)

tombol_edit_database.grid(row=3, column=0)
tombol_refresh_database.grid(row=3, column=1)

def displaySelectedItem(a):
    # Bersihkan Entry (Hapus isi nama, uang pelanggan, kembalian)
    name_entry.delete(0, "end")
    uang_pelanggan_entry.delete(0,"end")
    kembalian_entry.delete(0,"end")

    selectedItem = tabel_pencarian.selection()[0]
    name_entry.insert(0, tabel_pencarian.item(selectedItem)['values'][1])

tabel_pencarian.bind("<<TreeviewSelect>>", displaySelectedItem) #Menghubungkan tabel pencarian dengan fungsi displaySelectedItem()


# -------------------------- TABLE PEMBELIAN / Daftar barang yang di beli -------------------------------------------

tabel_pembelian = ttk.Treeview(frame_pembelian)

tabel_pembelian['columns'] = ('id', 'nama barang', 'jumlah', 'total harga')

tabel_pembelian.column("#0", width=0,  stretch="no")
tabel_pembelian.column("id",anchor="center", width=80)
tabel_pembelian.column("nama barang",anchor="center",width=80)
tabel_pembelian.column("jumlah",anchor="center",width=80)
tabel_pembelian.column("total harga",anchor="center",width=80)

tabel_pembelian.heading("#0",text="",anchor="center")
tabel_pembelian.heading("id",text="ID",anchor="center")
tabel_pembelian.heading("nama barang",text="Nama",anchor="center")
tabel_pembelian.heading("jumlah",text="Jumlah",anchor="center")
tabel_pembelian.heading("total harga",text="Total Harga",anchor="center")

tabel_pembelian.pack()

# --------------------------------------------------------------------------------------------------------------------

root.mainloop()
conn.close()