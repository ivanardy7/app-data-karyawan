# ---------- Imports ----------
import mysql.connector
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd

# ---------- DB Helpers ----------
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Password.1',
    database = 'database_karyawan'
    )

def fetch_all(query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cols = cur.column_names
    df = pd.DataFrame(rows, columns = cols)
    return rows, cols

def execute_commit(query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    return True

# ---------- Feature 1: Read ----------
def menu_read():
    while True:
        print("\n=== Data Karyawan ===")
        print("1) Tampilkan semua")
        print("2) Filter by department")
        print("3) Sort by salary (DESC)")
        print("4) Sort by join_date (ASC)")
        print("0) Kembali")
        choice = input("Pilih: ").strip()
        base = "SELECT employee_id, full_name, department, age, salary, join_date, status FROM employees"

        if choice == "1":
            q = base
            rows, cols = fetch_all(q)
            if not rows:
                print(" Data kosong.")
                break
            print(tabulate(rows, headers=cols, tablefmt="grid", intfmt=","))

        elif choice == "2":
            dept = input("Masukkan department (cth. IT/HR/Production/Sales/Finance): ").strip()
            q = base + " WHERE department = %s"
            rows, cols = fetch_all(q, (dept,))
            if not rows:
                print(" Data kosong.")
                break
            print(tabulate(rows, headers=cols, tablefmt="grid", intfmt=","))

        elif choice == "3":
            q = base + " ORDER BY salary DESC"
            rows, cols = fetch_all(q)
            if not rows:
                print(" Data kosong.")
                break
            print(tabulate(rows, headers=cols, tablefmt="grid", intfmt=","))

        elif choice == "4":
            q = base + " ORDER BY join_date ASC"
            rows, cols = fetch_all(q)
            if not rows:
                print(" Data kosong.")
                break
            print(tabulate(rows, headers=cols, tablefmt="grid", intfmt=","))

        elif choice == "0":
            break
        else:
            print("\nPilihan tidak valid, silahkan kembali")
        print("\n0) Kembali")
        input("Pilih: ")

# ---------- Feature 2: Statistik (mean) ----------
def menu_stats():
    while True:
        print("\n=== Statistik ===")
        print("Pilih kolom numeric:")
        print("1) Age")
        print("2) Salary")
        print("0) Kembali ke menu")
        choice = input("Pilih: ").strip()

        if choice == "1":
            while True:
                rows, _ = fetch_all(f"SELECT age FROM employees")
                values = [r[0] for r in rows] 
                mean_val = sum(values) / len(values)
                print(f"\nKolom: age")
                print(f"Count: {len(values)}")
                print(f"Mean : {mean_val:.2f}")
                print(f"Min  : {min(values)}")
                print(f"Max  : {max(values)}")
                print(f"Median: {np.median(values):.2f}")
                print("\n0) Kembali")
                input("Pilih: ")
                break
        if choice == "2":
            while True:
                rows, _ = fetch_all(f"SELECT salary FROM employees")
                values = [r[0] for r in rows] 
                mean_val = sum(values) / len(values)
                print(f"\nKolom: salary")
                print(f"Count: {len(values)}")
                print(f"Mean : {mean_val:.2f}")
                print(f"Min  : {min(values)}")
                print(f"Max  : {max(values)}")
                print(f"Median: {np.median(values):.2f}")
                print("\n0) Kembali")
                input("Pilih: ")
                break
        if choice == "0":
            return
        
        if not values:
            print(" Data kosong.")
            pause()
            return

        if choice not in ["1", "2","0"]:
            print(" Pilihan tidak valid.")
            pause()
            return

# ---------- Feature 3: Visualization ----------
def plot_categorical(col):
    rows, _ = fetch_all(f"SELECT {col}, COUNT(*) FROM employees GROUP BY {col}")
    if not rows:
        print(" Data kosong.")
        return

    labels = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    while True:
        print("\nPilih tipe visualisasi:")
        print("1) Bar plot")
        print("2) Pie chart")
        print("0) Kembali")
        print("ENTER) Kembali ke menu utama")
        c = input("Pilih: ").strip()

        if c == "1":
            plt.figure()
            plt.bar(labels, counts)
            plt.title(f"Distribusi {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.xticks(rotation=25)
            plt.tight_layout()
            plt.show()
            
        elif c == "2":
            plt.figure()
            plt.pie(counts, labels=labels, autopct="%1.1f%%")
            plt.title(f"Proporsi {col}")
            plt.tight_layout()
            plt.show()
            
        elif c == "0":
            return
        elif c == "":
            return ""
        else:
            print(" Pilihan tidak valid.")
    

def plot_histogram(col):
    rows, _ = fetch_all(f"SELECT {col} FROM employees")
    values = [r[0] for r in rows]
    if not values:
        print(" Data kosong.")
        return
    while True:
        bins = input("Jumlah bins histogram (mis. 5-20): ")
        if bins == "":
            return ""
        elif bins == "0":
            return
        elif bins.isdigit() :
            bins_val = int(bins)
            if 3<= bins_val <= 50:
                plt.figure()
                plt.hist(values, bins=bins_val)
                plt.title(f"Histogram {col}")
                plt.xlabel(col)
                plt.ylabel("Frekuensi")
                plt.tight_layout()
                plt.show()
                break

def menu_viz():
    
    while True:
        print("\n=== Visualisasi ===")
        print("1) Categorical (department/status)")
        print("2) Numerical (age/salary)")
        print("0) Kembali")
        choice = input("Pilih: ").strip()
        
        if choice == "1":
            while True:
                print("\nPilih kolom categorical:")
                print("1) Department")
                print("2) Status")
                print("0) Kembali")
                pick = input("Pilih: ").strip()
                if pick == "1":
                    wadah = plot_categorical("department")
                elif pick == "2":
                    wadah = plot_categorical("status")
                elif pick == "0":
                    break
                else:
                    print(" Pilihan tidak valid.")
                    continue
                if wadah == "":
                    return
                
        if choice == "2":
            while True:
                print("\nPilih kolom numerical:")
                print("1) Age")
                print("2) Salary")
                print("0) Kembali")
                print("ENTER) Kembali ke menu")
                pick = input("Pilih: ").strip()
                if pick == "1":
                    wadah = plot_histogram("age")
                elif pick == "2":
                    wadah = plot_histogram("salary")
                elif pick == "0":
                    break
                elif pick == "":
                    return
                else:
                    print(" Pilihan tidak valid.")
                    continue
                
        if choice == "0":
            return

# ---------- Feature 4: Add Data ----------
def menu_add():
    print("\n=== Tambah Data Karyawan ===")
    
    #----------------1) Nama ----------------
    while True:
        full_name = input("Nama lengkap: (cth. Ivan Ardy)").strip()
        if not full_name:
            print(" Nama tidak boleh kosong.")
            continue
        break
    #----------------2) Department ----------------
    while True:
        department = input("Department (IT/HR/Production/Sales/Finance): ").strip()
        if not department:
            print(" Department tidak boleh kosong.")
            continue
        break
    #---------------- 3) Age ----------------
    # 3) Age
    while True:
        s = input("Umur (17-65): ").strip()
        if not s.isdigit():
            print(" Masukan angka ")
            continue
        
        age = int(s)
        if age < 17 or age > 65:
            print(" Nilai minimal 17 dan maksimal 65")
            continue
        break
    #---------------- 4) Salary ----------------
    # 4) Salary
    while True:
        s = input("Gaji (>= 1000000): ").strip()
        if not s.isdigit():
            print(" Masukan angka ")
            continue
        
        salary = int(s)
        if salary < 1000000:
            print(" Nilai minimal 1000000")
            continue
        break
    #---------------- 5) Join Date ----------------
    while True:
        s = input("Tanggal masuk (DD-MM-YYYY): ").strip()
        if not s:
            print(" Tanggal tidak boleh kosong")
            continue
            
        try:
            join_date = datetime.strptime(s, "%d-%m-%Y").date()
            break 
            
        except ValueError:
            print(" Format salah! Gunakan DD-MM-YYYY (Contoh: 14-03-2024)")
    #---------------- 6) Status ----------------
    status = input("Status (active/resigned) [default active]: ").strip().lower()
    if status == "":
        status = "active"
    if status not in ["active", "resigned"]:
        print(" Status harus 'active' atau 'resigned'.")
        input()
        return
    #---------------- 7) Confirmation ----------------
    confirm = input("Yakin simpan data? (y/n): ").strip().lower()
    if confirm != "y":
        print(" batal ")
        input()
        return

    q = """
    INSERT INTO employees (full_name, department, age, salary, join_date, status)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    ok = execute_commit(q, (full_name, department, age, salary, join_date, status))
    if ok:
        print(" Data berhasil ditambahkan! ")

# ---------- Main Menu ----------
def main_menu():
    while True:
        print("\n===============================")
        print("       APP DATA KARYAWAN ")
        print("===============================")
        print("1) Data Karyawan")
        print("2) Statistik")
        print("3) Visualisasi")
        print("4) Tambah Data Karyawan")
        print("0) Keluar Dari App")

        choice = input("Pilih menu: ").strip()
        if choice == "1":
            menu_read()
        elif choice == "2":
            menu_stats()
        elif choice == "3":
            menu_viz()
        elif choice == "4":
            menu_add()
        elif choice == "0":
            print("\n-----Sampai Jumpa!-----")
            break
        else:
            print(" Menu tidak valid. Coba lagi.")

if __name__ == "__main__":
    main_menu()