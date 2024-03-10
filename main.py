import os
import shutil
import winreg
import tkinter as tk
from tkinter import messagebox

def delete_folder(path):
    try:
        shutil.rmtree(path)
        print(f"Deleted folder: {path}")
    except Exception as e:
        print(f"Error deleting folder {path}: {e}")

def delete_registry_key(hive, key):
    try:
        # Tenta abrir a chave de registro
        registry_key = winreg.OpenKey(hive, key, 0, winreg.KEY_ALL_ACCESS)

        # Obtém o nome da chave de registro a partir do caminho
        key_name = key.split("\\")[-1]

        # Tenta excluir a chave de registro
        winreg.DeleteKey(hive, key)

        print(f"Deleted registry key: {key}")
    except Exception as e:
        print(f"Error deleting registry key {key}: {e}")
    finally:
        # Fecha a chave de registro, se estiver aberta
        try:
            winreg.CloseKey(registry_key)
        except:
            pass

def remove_sql_evidences():
    # SQL Server registry keys
    sql_registry_keys = [
        r"SOFTWARE\Microsoft\Microsoft SQL Server",
        r"SOFTWARE\WOW6432Node\Microsoft\Microsoft SQL Server"
    ]

    # Uninstall SQL Server instances
    for key in sql_registry_keys:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as reg_key:
                subkey_num = winreg.QueryInfoKey(reg_key)[0]
                for i in range(subkey_num):
                    subkey_name = winreg.EnumKey(reg_key, i)
                    if subkey_name.startswith("MSSQL"):
                        subkey_path = os.path.join(key, subkey_name)
                        delete_registry_key(winreg.HKEY_LOCAL_MACHINE, subkey_path)
                        print(f"Uninstalled SQL Server instance: {subkey_name}")
        except Exception as e:
            print(f"Error accessing registry key {key}: {e}")

    messagebox.showinfo("Success", "All SQL Server evidences have been removed.")

def on_remove_click():
    confirm = messagebox.askyesno("Confirm", "This action will remove all SQL Server evidences from this machine. Continue?")
    if confirm:
        remove_sql_evidences()

# Create the GUI
root = tk.Tk()
root.title("SQL Server Evidence Remover")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Click below to remove all SQL Server evidences from this machine.")
label.pack(padx=10, pady=10)

remove_button = tk.Button(frame, text="Remove SQL Evidences", command=on_remove_click)
remove_button.pack(padx=10, pady=5)

root.mainloop()
