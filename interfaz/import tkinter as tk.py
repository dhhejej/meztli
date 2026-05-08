import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import os

# =======================
#   CONEXIÓN MYSQL
# =======================
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="rancho"
    )

class ConexionMySQL:
    def __enter__(self):
        self.con = obtener_conexion()
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.cursor.close()
        self.con.close()

# =======================
#   LOGIN
# =======================
def verificar_usuario(usuario, contraseña):
    try:
        con = obtener_conexion()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=%s AND contraseña=%s", (usuario, contraseña))
        r = cur.fetchone()
        con.close()
        return r is not None
    except:
        return False

def mostrar_login():
    login = tk.Tk()
    login.title("Login - Floricultura")
    login.geometry("350x250")
    login.configure(bg="#fce4ec")

    tk.Label(login, text="🌸 FLORICULTURA 🌸", font=("Segoe UI", 16, "bold"), bg="#fce4ec").pack(pady=15)
    tk.Label(login, text="Usuario", bg="#fce4ec").pack()
    user = tk.Entry(login); user.pack()
    tk.Label(login, text="Contraseña", bg="#fce4ec").pack()
    pwd = tk.Entry(login, show="*"); pwd.pack()

    def ingresar():
        if verificar_usuario(user.get(), pwd.get()):
            login.destroy()
            ventana_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    tk.Button(login, text="Ingresar", command=ingresar, bg="#ec407a", fg="white", width=20).pack(pady=20)
    login.mainloop()

# =======================
#   VENTANA PRINCIPAL
# =======================
def ventana_principal():
    root = tk.Tk()
    root.title("Sistema de Floricultura")
    root.geometry("900x600")

    fondo = tk.Label(root)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    # Intentar cargar fondo principal
    if os.path.exists("R.jpg"):
        img = Image.open("R.jpg").resize((900, 600), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        fondo.config(image=img_tk)
        fondo.image = img_tk # Referencia para evitar que desaparezca
    else:
        fondo.config(bg="#f8bbd0")

    lbl_titulo = tk.Label(root, text="SISTEMA DE FLORICULTURA", 
                          font=("Segoe UI", 28, "bold"), 
                          fg="#880e4f", bg="white", padx=20, pady=10)
    lbl_titulo.place(relx=0.5, y=60, anchor="center")

    botones = [
        ("Registrar Cliente", registrar_cliente),
        ("Registrar Flor", registrar_flor),
        ("Gestionar Flores", gestionar_flores),
        ("Realizar Venta", realizar_venta),
        ("Historial de Ventas", mostrar_historial)
    ]

    y = 180
    for texto, cmd in botones:
        tk.Button(root, text=texto, command=cmd, bg="#ec407a", fg="white", 
                  font=("Segoe UI", 14, "bold"), width=25).place(relx=0.5, y=y, anchor="center")
        y += 65
    
    root.mainloop()

# =======================
#   REGISTRAR CLIENTE
# =======================
def registrar_cliente():
    win = tk.Toplevel()
    win.title("Registrar Cliente")
    win.geometry("400x300")
    
    fondo = tk.Label(win)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    if os.path.exists("rosas-1340x755.jpg"):
        img = Image.open("rosas-1340x755.jpg").resize((400, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        fondo.config(image=img_tk)
        fondo.image = img_tk # IMPORTANTE: Mantener referencia
    else:
        fondo.config(bg="#fce4ec")

    cont = tk.Frame(win, bg="white", padx=10, pady=10)
    cont.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(cont, text="Nombre:", bg="white").pack()
    n = tk.Entry(cont); n.pack()
    tk.Label(cont, text="Contacto:", bg="white").pack()
    c = tk.Entry(cont); c.pack()

    def g():
        with ConexionMySQL() as cur: 
            cur.execute("INSERT INTO clientes (nombre, contacto) VALUES (%s,%s)", (n.get(), c.get()))
        messagebox.showinfo("Éxito", "Cliente Guardado")
        win.destroy()
    tk.Button(cont, text="Guardar", command=g, bg="#ec407a", fg="white").pack(pady=10)

# =======================
#   REGISTRAR FLOR
# =======================
def registrar_flor():
    win = tk.Toplevel()
    win.title("Registrar Flor")
    win.geometry("400x400")
    
    fondo = tk.Label(win)
    fondo.place(x=0, y=0, relwidth=1, relheight=1)
    
    if os.path.exists("istockphoto-984169074-612x612.jpg"):
        img = Image.open("istockphoto-984169074-612x612.jpg").resize((400, 400), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        fondo.config(image=img_tk)
        fondo.image = img_tk # IMPORTANTE: Mantener referencia
    else:
        fondo.config(bg="#fce4ec")

    cont = tk.Frame(win, bg="white", padx=10, pady=10)
    cont.place(relx=0.5, rely=0.5, anchor="center")

    entradas = {}
    for campo in ["Nombre", "Tipo", "Cantidad", "Precio"]:
        tk.Label(cont, text=campo, bg="white").pack()
        e = tk.Entry(cont); e.pack()
        entradas[campo] = e

    def g():
        with ConexionMySQL() as cur: 
            cur.execute("INSERT INTO flores (nombre,tipo,cantidad,precio) VALUES (%s,%s,%s,%s)", 
                        (entradas["Nombre"].get(), entradas["Tipo"].get(), entradas["Cantidad"].get(), entradas["Precio"].get()))
        messagebox.showinfo("Éxito", "Flor Guardada")
        win.destroy()
    tk.Button(cont, text="Guardar", command=g, bg="#ec407a", fg="white").pack(pady=10)

# =======================
#   REALIZAR VENTA CON ZOOM
# =======================
def realizar_venta():
    win = tk.Toplevel()
    win.title("Venta y Catálogo")
    win.geometry("550x850")
    win.configure(bg="white")

    frame_form = tk.LabelFrame(win, text=" Datos de Venta ", bg="white")
    frame_form.pack(pady=10, fill="x", padx=20)

    tk.Label(frame_form, text="Cliente:", bg="white").grid(row=0, column=0, padx=5)
    cb_cliente = ttk.Combobox(frame_form, width=30); cb_cliente.grid(row=0, column=1, pady=5)
    tk.Label(frame_form, text="Flor:", bg="white").grid(row=1, column=0, padx=5)
    cb_flor = ttk.Combobox(frame_form, width=30); cb_flor.grid(row=1, column=1, pady=5)
    tk.Label(frame_form, text="Cant:", bg="white").grid(row=2, column=0, padx=5)
    cant = tk.Entry(frame_form); cant.grid(row=2, column=1, pady=5)

    try:
        con = obtener_conexion(); cur = con.cursor()
        cur.execute("SELECT id, nombre FROM clientes"); cb_cliente["values"] = [f"{i}-{n}" for i, n in cur.fetchall()]
        cur.execute("SELECT id, nombre FROM flores"); cb_flor["values"] = [f"{i}-{n}" for i, n in cur.fetchall()]
        con.close()
    except: pass

    def vender():
        try:
            id_cli = int(cb_cliente.get().split("-")[0]); id_flo = int(cb_flor.get().split("-")[0]); c = int(cant.get())
            with ConexionMySQL() as cur:
                cur.execute("SELECT precio FROM flores WHERE id=%s", (id_flo,))
                p = cur.fetchone()[0]; total = p * c
                cur.execute("INSERT INTO ventas (cliente_id, total) VALUES (%s,%s)", (id_cli, total))
                v_id = cur.lastrowid
                cur.execute("INSERT INTO detalle_venta VALUES (%s,%s,%s)", (v_id, id_flo, c))
                cur.execute("UPDATE flores SET cantidad=cantidad-%s WHERE id=%s", (c, id_flo))
            messagebox.showinfo("Éxito", f"Total: ${total}")
            win.destroy()
        except: messagebox.showerror("Error", "Revisar datos")

    tk.Button(win, text="REGISTRAR VENTA", command=vender, bg="#4CAF50", fg="white", font="bold").pack()

    # IMAGEN DEL CATÁLOGO
    img_path = "1098d74d1c71f7a7485cec4c7c1cb758.jpg" # Nombre del archivo que subiste
    if os.path.exists(img_path):
        img_raw = Image.open(img_path)
        img_thumb = img_raw.resize((480, 500), Image.LANCZOS)
        photo_thumb = ImageTk.PhotoImage(img_thumb)
        
        def ver_grande(event):
            zoom_win = tk.Toplevel()
            img_big = Image.open(img_path).resize((800, 950), Image.LANCZOS)
            photo_big = ImageTk.PhotoImage(img_big)
            lbl_big = tk.Label(zoom_win, image=photo_big)
            lbl_big.image = photo_big # Referencia
            lbl_big.pack()

        lbl_img = tk.Label(win, image=photo_thumb, cursor="hand2")
        lbl_img.image = photo_thumb # Referencia
        lbl_img.pack(pady=10)
        lbl_img.bind("<Button-1>", ver_grande)
    else:
        tk.Label(win, text="⚠️ Falta imagen: " + img_path, fg="red").pack()

# --- Funciones de Gestión ---
def gestionar_flores():
    win = tk.Toplevel(); win.geometry("500x300")
    t = ttk.Treeview(win, columns=(1,2,3,4,5), show="headings")
    for i, col in enumerate(["ID","Nombre","Tipo","Stock","Precio"],1): t.heading(i, text=col)
    t.pack(fill="both", expand=True)
    with ConexionMySQL() as cur:
        cur.execute("SELECT * FROM flores")
        for r in cur.fetchall(): t.insert("", "end", values=r)

def mostrar_historial():
    win = tk.Toplevel()
    win.title("Historial de Ventas")
    win.geometry("750x400")

    frame_buscar = tk.Frame(win)
    frame_buscar.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_buscar, text="Buscar por flor:").pack(side="left")
    buscar = tk.Entry(frame_buscar, width=30)
    buscar.pack(side="left", padx=5)

    frame_tabla = tk.Frame(win)
    frame_tabla.pack(fill="both", expand=True)

    t = ttk.Treeview(
        frame_tabla,
        columns=("ID", "Fecha", "Cliente", "Flor", "Cantidad", "Total"),
        show="headings"
    )

    for col in ("ID", "Fecha", "Cliente", "Flor", "Cantidad", "Total"):
        t.heading(col, text=col)
        t.column(col, anchor="center")

    t.pack(fill="both", expand=True)

    def cargar_datos(filtro=""):
        for item in t.get_children():
            t.delete(item)

        with ConexionMySQL() as cur:
            sql = """
            SELECT v.id, v.fecha, c.nombre, f.nombre, d.cantidad, v.total
            FROM ventas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN detalle_venta d ON v.id = d.venta_id
            JOIN flores f ON d.flor_id = f.id
            WHERE f.nombre LIKE %s
            """
            cur.execute(sql, (f"%{filtro}%",))
            for r in cur.fetchall():
                t.insert("", "end", values=r)

    def buscar_flor():
        cargar_datos(buscar.get())

    tk.Button(
        frame_buscar,
        text="Buscar",
        command=buscar_flor,
        bg="#ec407a",
        fg="white"
    ).pack(side="left", padx=5)

    # Cargar todo al inicio
    cargar_datos()

if __name__ == "__main__":
    mostrar_login() 