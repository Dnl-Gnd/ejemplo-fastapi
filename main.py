#npx plugins add vercel/vercel-plugin
#pip install fastapi

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(
    title="Vercel + FastAPI",
    description="Vercel + FastAPI",
    version="1.0.0",
)


@app.get("/api/data")
def get_sample_data():
    return {
        "data": [
            {"id": 1, "name": "Sample Item 1", "value": 100},
            {"id": 2, "name": "Sample Item 2", "value": 200},
            {"id": 3, "name": "Sample Item 3", "value": 300}
        ],
        "total": 3,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    return {
        "item": {
            "id": item_id,
            "name": "Sample Item " + str(item_id),
            "value": item_id * 100
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generador de Código QR</title>
        <link rel="icon" type="image/x-icon" href="/favicon.ico">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
                background-color: #0b1220;
                color: #f7f8fb;
                line-height: 1.6;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            header {
                border-bottom: 1px solid #25305c;
            }
            
            nav {
                max-width: 1100px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 1.25rem 1.5rem;
            }
            
            .logo {
                font-size: 1.35rem;
                font-weight: 700;
                color: #fff;
                text-decoration: none;
            }
            
            main {
                flex: 1;
                max-width: 1100px;
                margin: 0 auto;
                padding: 3rem 1.5rem;
                display: flex;
                flex-direction: column;
                gap: 2rem;
            }
            
            .hero {
                text-align: center;
            }
            
            h1 {
                font-size: 2.75rem;
                font-weight: 800;
                color: #fff;
                margin-bottom: 0.75rem;
            }
            
            p {
                color: #c5cbdc;
                font-size: 1rem;
                max-width: 760px;
                margin: 0 auto;
            }
            
            .section {
                background-color: #11182e;
                border: 1px solid #22305b;
                border-radius: 18px;
                padding: 1.75rem;
            }
            
            .section h2 {
                margin-bottom: 1rem;
                color: #f1f5ff;
                font-size: 1.5rem;
            }
            
            .section pre {
                background-color: #0f172a;
                color: #e2e8f0;
                border-radius: 14px;
                padding: 1rem;
                overflow-x: auto;
                font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', monospace;
                font-size: 0.92rem;
                line-height: 1.5;
                white-space: pre-wrap;
                word-break: break-word;
            }
            
            .instructions {
                display: grid;
                gap: 1rem;
            }
            
            .badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.45rem 0.85rem;
                border-radius: 999px;
                background: #1b2f68;
                color: #dbeafe;
                font-size: 0.9rem;
                font-weight: 600;
            }
            
            @media (max-width: 760px) {
                nav {
                    flex-direction: column;
                    align-items: flex-start;
                }

                h1 {
                    font-size: 2.25rem;
                }
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Generador de Código QR</a>
            </nav>
        </header>
        <main>
            <section class="hero">
                <h1>Arranque del proyecto</h1>
                <p>Esta página muestra el código y las instrucciones para ejecutar una pequeña aplicación de escritorio en Tkinter que genera, guarda y lee códigos QR.</p>
            </section>

            <section class="section">
                <h2>Instalación requerida</h2>
                <div class="instructions">
                    <pre>pip install qrcode[pil]
pip install Pillow
pip install opencv-python
pip install opencv-contrib-python</pre>
                </div>
            </section>

            <section class="section">
                <h2>Cómo ejecutar</h2>
                <div class="instructions">
                    <pre>python app.py</pre>
                </div>
            </section>

            <section class="section">
                <h2>Código de ejemplo</h2>
                <pre>import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import ImageTk, Image
import cv2

imagen_qr = None
imagen_pil = None
camara_activa = False
cap = None
detector = cv2.QRCodeDetector()

def generate_qr():
    global imagen_qr, imagen_pil
    link = entrada_link.get().strip()

    if not link:
        messagebox.showerror("Error", "Por favor, ingresa un enlace.")
        return

    qr = qrcode.make(link)
    imagen_pil = qr
    imagen_qr = ImageTk.PhotoImage(qr.resize((250, 250)))
    etiqueta_imagen.config(image=imagen_qr)
    boton_descargar.config(state="normal")


def descargar_qr():
    if imagen_pil is None:
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("imagen PNG", "*.png")],
        title="Guardar código QR"
    )

    if ruta:
        imagen_pil.save(ruta)
        messagebox.showinfo("Listo", f"Código QR guardado exitosamente en {ruta}")


def leer_desde_imagen():
    ruta = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")],
        title="Seleccionar imagen con código QR"
    )

    if not ruta:
        return

    imagen = cv2.imread(ruta)
    contenido, _, _ = detector.detectAndDecode(imagen)

    if contenido:
        etiqueta_resultado.config(text=f"Contenido: {contenido}")
    else:
        messagebox.showwarning("Sin resultado", "No se encontró ningún código QR en la imagen.")


def escanear_camara():
    global camara_activa, cap

    if not camara_activa:
        return

    ret, frame = cap.read()

    if ret:
        contenido, _, _ = detector.detectAndDecode(frame)

        if contenido:
            etiqueta_resultado.config(text=f"Contenido: {contenido}")
            detener_camara()
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb).resize((250, 250))
        foto = ImageTk.PhotoImage(img)
        etiqueta_imagen.config(image=foto)
        etiqueta_imagen.image = foto

    ventana.after(30, escanear_camara)


def detener_camara():
    global camara_activa, cap
    camara_activa = False
    if cap:
        cap.release()
        cap = None
    etiqueta_resultado.config(image="")

ventana = tk.Tk()
ventana.title("Generador de Código QR")
ventana.geometry("400x600")
ventana.resizable(False, False)

# ... resto del código del GUI ...
                </pre>
            </section>
        </main>
    </body>
    </html>
    """
