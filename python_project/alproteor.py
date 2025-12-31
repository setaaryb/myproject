#SURUH TUH AI BIKIN SYSTEM KEK GINI JAM 4 PAGI DAN GAK EROR
#SOURCE CODE BY S4IMOE

import os, sqlite3

def c():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = """
                    ███████████                   
                ███████████████████               
              █████▓▓▓▓▓▒▒▒▓▓▓▓██████             
            ████▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓█████           
          ████▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓████          
         ████▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓████         
        ███████▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▒▓▓▓▓█▓▓███        
        ███▒▒▒▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▒▒▒▓███       
       ███▓▒▒▒▒▒▒▓▓█████▓▓█████▓▓▒▒▒▒▒▒▒███       
       ███▒▒▒▒▒▒▒▒▒▒▓████████▓▒▒▒▒▒▒▒▒▒▒▓██       
       ███▒▒▒▒▒▒▒▒▒▒▒▓██████▓▒▒▒▒▒▒▒▒▒▒▒▓██     
       ███▓▒▒▒▒▒▒▒▒▒▒▒▓████▓▒▒▒▒▒▒▒▒▒▒▒▒▓██       
        ██▓▒▒▒▒▒▒▒▒▒▒▒▒▓██▓▒▒▒▒▒▒▒▒▒▒▒▒▓███       
        ███▓▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒████       
         ███▓▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓███        
          ███▓▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▓████         
           ████▓▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▓▓████          
            █████▓▓▒▒▒▒▒▓▓▓▒▒▒▒▓▓█████            
               ██████▓▓▓█▓▓▓▓███████              
                 ████████████████                

           ██████  ███    ██ ███    ███ 
           ██   ██ ████   ██ ████  ████ 
           ██████  ██ ██  ██ ██ ████ ██ 
           ██      ██  ██ ██ ██  ██  ██ 
           ██      ██   ████ ██      ██\n"""

conn = sqlite3.connect('mekaar_system.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kelompok (
    id_kelompok INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kelompok TEXT NOT NULL,
    desa TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nasabah (
    id_nasabah INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    nik TEXT UNIQUE NOT NULL,
    id_kelompok INTEGER,
    plafon_pinjaman REAL,
    FOREIGN KEY (id_kelompok) REFERENCES kelompok (id_kelompok)
)""")

cursor.execute("SELECT COUNT(*) FROM kelompok")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO kelompok (nama_kelompok, desa) VALUES (?, ?)",
        ("DEFAULT", "DEFAULT")
    )

conn.commit()
conn.close()

def add_kelompok(nama, desa):
    conn = sqlite3.connect('mekaar_system.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO kelompok (nama_kelompok, desa) VALUES (?, ?)",
        (nama, desa))
    conn.commit()
    conn.close()
    print("---------------------------------------------------")
    print(f"[ PNM-MEKAAR ] Kelompok '{nama}' berhasil didaftarkan.")

def add_nasabah(nama, nik, id_kelompok, plafon,id_k):
    try:
        conn = sqlite3.connect('mekaar_system.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nasabah (nama, nik, id_kelompok, plafon_pinjaman)
            VALUES (?, ?, ?, ?)
        """, (nama, nik, id_kelompok, plafon))
        conn.commit()
        print("---------------------------------------------------")
        print(f"[ PNM-MEKAAR ] Nasabah '{nama}' berhasil ditambahkan ke kelompok ID {id_kelompok}.")
    except sqlite3.IntegrityError:
        print("---------------------------------------------------")
        print("[ PNM-MEKAAR ] Error: NIK sudah terdaftar!")
    finally:
        conn.close()

def hapus_kelompok(id_kelompok):
    conn = sqlite3.connect('mekaar_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM nasabah WHERE id_kelompok = ?", (id_kelompok,))
    if cursor.fetchone()[0] > 0:
        print("[ PNM-MEKAAR ] Kelompok tidak bisa dihapus (masih ada nasabah).\n")
    else:
        cursor.execute("DELETE FROM kelompok WHERE id_kelompok = ?", (id_kelompok,))
        conn.commit()
        print("[ PNM-MEKAAR ] Kelompok berhasil dihapus.\n")
    conn.close()

def hapus_nasabah(id_nasabah):
    conn = sqlite3.connect('mekaar_system.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nasabah WHERE id_nasabah = ?", (id_nasabah,))
    conn.commit()
    if cursor.rowcount == 0:
        print("[ PNM-MEKAAR ] ID nasabah tidak ditemukan.\n")
    else:
        print("[ PNM-MEKAAR ] Nasabah berhasil dihapus.\n")
    conn.close()

def tampilkan_semua_nasabah():
    conn = sqlite3.connect('mekaar_system.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.id_nasabah, n.nama, k.nama_kelompok, n.plafon_pinjaman
        FROM nasabah n
        JOIN kelompok k ON n.id_kelompok = k.id_kelompok""")
    rows = cursor.fetchall()
    print("\n-------------- DAFTAR NASABAH MEKAAR --------------")
    print(f"{'ID':<4} {'Nama':<15} {'Kelompok':<15} {'Plafon':<10}")
    print("---------------------------------------------------")
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<15} {row[2]:<15} Rp{row[3]:,.0f}")
    conn.close()

def import_db(nama_db):
    conn1 = sqlite3.connect(nama_db)
    cur1 = conn1.cursor()
    conn2 = sqlite3.connect('mekaar_system.db')
    cur2 = conn2.cursor()
    cur1.execute("SELECT nama, nik, id_kelompok, plafon_pinjaman FROM nasabah")
    data = cur1.fetchall()
    for d in data:
        try:
            cur2.execute(
                "INSERT INTO nasabah VALUES (NULL, ?, ?, ?, ?)",
                d
            )
        except:
            pass
    conn2.commit()
    conn1.close()
    conn2.close()
    print("[ PNM-MEKAAR ] Import selesai.\n")

def tampilkan_kelompok():
    conn = sqlite3.connect('mekaar_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_kelompok, nama_kelompok, desa FROM kelompok")
    rows = cursor.fetchall()
    print("\n-------------- DAFTAR KELOMPOK --------------")
    print(f"{'ID':<4} {'Kelompok':<15} {'Desa':<15}")
    print("---------------------------------------------")
    for r in rows:
        print(f"{r[0]:<4} {r[1]:<15} {r[2]:<15}")
    conn.close()

def main():
    while True:
        c()
        print(banner)
        print("---------------------------------------------------")
        print("[1]. TAMBAH NASABAH\n[2]. TAMBAH KELOMPOK\n[3]. TAMPILKAN DAFTAR NASABAH\n[4]. TAMPILKAN DAFTAR KELOMPOK\n[5]. HAPUS DATA NASABAH & KELOMPOK\n---------------------------------------------------\n[E]. KELUAR       [I]. IMPORT DB\n")
        menu_input = input("[ PNM-MEKAAR ] Pilihan : ")
        if menu_input == "1":
            c()
            print(banner)
            id_k = int(input("[ PNM-MEKAAR ] Pilih ID Kelompok : "))
            nama_n = input("[ PNM-MEKAAR ] Nama Nasabah: ")
            nik_n = input("[ PNM-MEKAAR ] NIK: ")
            plafon_n = float(input("[ PNM-MEKAAR ] Plafon Pinjam: "))
            add_nasabah(nama_n, nik_n, 1, plafon_n,id_k)
            input("\n[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
        elif menu_input == "2":
            c()
            print(banner)
            nama_k = input("[ PNM-MEKAAR ] Nama Kelompok : ")
            nama_d = input("[ PNM-MEKAAR ] Desa : ")
            add_kelompok(nama_k, nama_d)
            input("\n[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
        elif menu_input == "3":
            c()
            print(banner)
            tampilkan_semua_nasabah()
            print("---------------------------------------------------")
            input("\n[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
        elif menu_input == "4":
            c()
            print(banner)
            tampilkan_kelompok()
            print("---------------------------------------------")
            input("\n[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
        elif menu_input == "5":
            c()
            print(banner)
            print("---------------------------------------------------")
            print("[1]. DELETE NASABAH\n[2]. DELETE KELOMPOK")
            print("---------------------------------------------------")
            del_input = input("[ PNM-MEKAAR ] Pilihan Delete : ")
            if del_input =="1":
                c()
                print(banner)
                tampilkan_semua_nasabah()
                print("---------------------------------------------------")
                id_h = int(input("[ PNM-MEKAAR ] ID Nasabah yang dihapus : "))
                hapus_nasabah(id_h)
                input("[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
            elif del_input == "2":
                c()
                print(banner)
                tampilkan_kelompok()
                print("---------------------------------------------------")
                id_k = int(input("[ PNM-MEKAAR ] ID Kelompok yang dihapus : "))
                hapus_kelompok(id_k)
                input("[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
            else:
                return main()
        elif menu_input.lower() == "i":
            c()
            print(banner)
            nama_db = input("[ PNM-MEKAAR ] Nama file database (hanya nama) : ")
            db_file = f"{nama_db}.db"
            import_db(db_file)
            input("[ PNM-MEKAAR ] Tekan ENTER untuk kembali...")
        elif menu_input.lower() == "e":
            c()
            break
        else:
            return main()

if __name__ == "__main__":
    main()