#npx plugins add vercel/vercel-plugin
#pip install fastapi

import qrcode
import io
from fastapi.responses import StreamingResponse
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


@app.get("/api/qr")
def generate_qr(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=12,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


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
                background: radial-gradient(circle at top left, #2d66ff 0%, #091026 40%),
                            radial-gradient(circle at bottom right, #0fb2a5 0%, transparent 35%);
                color: #ecf2ff;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 2rem;
            }

            .container {
                width: min(960px, 100%);
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(16px);
                border-radius: 28px;
                padding: 2rem;
                box-shadow: 0 30px 80px rgba(4, 9, 28, 0.45);
            }

            header {
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
                text-align: center;
                margin-bottom: 1.75rem;
            }

            h1 {
                font-size: clamp(2rem, 4vw, 3rem);
                letter-spacing: -0.04em;
            }

            p {
                color: #cbd6ff;
                max-width: 760px;
                margin: 0 auto;
                line-height: 1.8;
            }

            .grid {
                display: grid;
                grid-template-columns: 1.2fr 0.8fr;
                gap: 1.5rem;
            }

            .card {
                background: rgba(14, 26, 64, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                padding: 1.5rem;
            }

            .card h2 {
                margin-bottom: 1rem;
                font-size: 1.2rem;
                color: #f5f9ff;
            }

            label {
                display: block;
                margin-bottom: 0.65rem;
                color: #a8b8ff;
                font-size: 0.96rem;
            }

            input[type=text], input[type=file] {
                width: 100%;
                padding: 0.95rem 1rem;
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.12);
                background: rgba(255, 255, 255, 0.05);
                color: #f8fbff;
                font-size: 1rem;
            }

            button {
                width: 100%;
                margin-top: 1rem;
                padding: 0.95rem 1rem;
                border: none;
                border-radius: 14px;
                background: linear-gradient(135deg, #5d8cff 0%, #2e58ff 100%);
                color: white;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 18px 35px rgba(45, 102, 255, 0.28);
            }

            button.secondary {
                background: rgba(255, 255, 255, 0.08);
                color: #dce6ff;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }

            #qr-output {
                display: grid;
                place-items: center;
                gap: 1rem;
                min-height: 330px;
            }

            #qrCanvas {
                width: 250px;
                height: 250px;
                background: white;
                border-radius: 20px;
            }

            #result {
                margin-top: 1rem;
                color: #c0d4ff;
                min-height: 1.4rem;
                text-align: center;
                font-size: 0.96rem;
            }

            .button-row {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.75rem;
                margin-bottom: 1rem;
            }

            .camera {
                margin-top: 1rem;
                border-radius: 18px;
                overflow: hidden;
                background: #0f1b41;
                min-height: 260px;
                display: grid;
                gap: 1rem;
                padding: 1rem;
            }

            video,
            #photoCanvas {
                width: 100%;
                height: auto;
                border-radius: 18px;
                display: block;
                background: #061124;
            }

            #photoCanvas {
                display: none;
            }

            @media (max-width: 860px) {
                .grid {
                    grid-template-columns: 1fr;
                }
            }
                .grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Generador y lector de Código QR</h1>
                <p>Usa esta aplicación directamente en el navegador para generar un código QR, descargarlo y leer el contenido desde una imagen o cámara.</p>
            </header>

            <div class="grid">
                <div class="card">
                    <h2>Generar QR</h2>
                    <label for="linkInput">Enlace o texto</label>
                    <input id="linkInput" type="text" placeholder="Ingresa un enlace o texto" />
                    <button id="generateBtn">Generar Código QR</button>
                    <button id="downloadBtn" class="secondary" disabled>Descargar QR</button>
                    <div id="result"></div>
                </div>

                <div class="card" id="qr-output">
                    <canvas id="qrCanvas"></canvas>
                </div>
            </div>

            <div class="grid" style="margin-top: 1.5rem; gap: 1.5rem;">
                <div class="card">
                    <h2>Leer desde imagen</h2>
                    <label for="fileInput">Selecciona una imagen con código QR</label>
                    <input id="fileInput" type="file" accept="image/*" />
                    <button id="scanFileBtn" class="secondary">Leer Imagen</button>
                    <div id="fileResult"></div>
                </div>

                <div class="card">
                    <h2>Escanear con cámara</h2>
                    <div class="button-row">
                        <button id="cameraActionBtn" class="secondary">Iniciar Cámara</button>
                        <button id="photoActionBtn" class="secondary" disabled>Tomar Foto</button>
                    </div>
                    <div class="camera">
                        <video id="cameraVideo" playsinline></video>
                        <canvas id="photoCanvas"></canvas>
                    </div>
                    <div id="cameraResult"></div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
        <script>
            const linkInput = document.getElementById('linkInput');
            const generateBtn = document.getElementById('generateBtn');
            const downloadBtn = document.getElementById('downloadBtn');
            const qrCanvas = document.getElementById('qrCanvas');
            const result = document.getElementById('result');
            const fileInput = document.getElementById('fileInput');
            const scanFileBtn = document.getElementById('scanFileBtn');
            const fileResult = document.getElementById('fileResult');
            const cameraActionBtn = document.getElementById('cameraActionBtn');
            const photoActionBtn = document.getElementById('photoActionBtn');
            const cameraVideo = document.getElementById('cameraVideo');
            const photoCanvas = document.getElementById('photoCanvas');
            const cameraResult = document.getElementById('cameraResult');

            let cameraStream = null;
            let cameraActive = false;
            let photoState = 'none';

            function isUrl(text) {
                return /^(https?:\\/\\/)[^\\s]+$/i.test(text.trim());
            }

            function showResult(node, text, isError = false) {
                node.innerHTML = '';
                node.style.color = isError ? '#ff8d8d' : '#c0d4ff';
                const trimmed = text.trim();

                if (trimmed.startsWith('Contenido: ')) {
                    const value = trimmed.slice(11).trim();
                    const prefix = document.createTextNode('Contenido: ');
                    node.appendChild(prefix);
                    if (isUrl(value)) {
                        const link = document.createElement('a');
                        link.href = value;
                        link.textContent = value;
                        link.target = '_blank';
                        link.rel = 'noopener noreferrer';
                        link.style.color = '#7ac7ff';
                        link.style.textDecoration = 'underline';
                        node.appendChild(link);
                        return;
                    }
                }

                if (isUrl(trimmed)) {
                    const link = document.createElement('a');
                    link.href = trimmed;
                    link.textContent = trimmed;
                    link.target = '_blank';
                    link.rel = 'noopener noreferrer';
                    link.style.color = '#7ac7ff';
                    link.style.textDecoration = 'underline';
                    node.appendChild(link);
                    return;
                }

                node.textContent = text;
            }

            let qrImageUrl = null;

            function generateQRCode() {
                const value = linkInput.value.trim();
                if (!value) {
                    showResult(result, 'Ingresa un enlace o texto antes de generar.', true);
                    return;
                }

                const url = '/api/qr?data=' + encodeURIComponent(value);

                const img = new Image();
                img.onload = function () {
                    qrCanvas.width = img.naturalWidth;
                    qrCanvas.height = img.naturalHeight;
                    qrCanvas.style.width = '300px';
                    qrCanvas.style.height = '300px';
                    const ctx = qrCanvas.getContext('2d');
                    ctx.imageSmoothingEnabled = false;
                    ctx.drawImage(img, 0, 0);
                    qrImageUrl = url;
                    downloadBtn.disabled = false;
                    showResult(result, 'QR generado correctamente. Puedes descargarlo.', false);
                };
                img.onerror = function () {
                    showResult(result, 'Error al generar el código QR desde el servidor.', true);
                };
                img.src = url;
            }

            function downloadQRCode() {
                const link = document.createElement('a');
                link.href = qrCanvas.toDataURL('image/png');
                link.download = 'codigo-qr.png';
                link.click();
            }

            function decodeQRFromImage(imageData) {
                const code = jsQR(imageData.data, imageData.width, imageData.height);
                return code ? code.data : null;
            }

            function readFromFile() {
                const file = fileInput.files[0];
                if (!file) {
                    showResult(fileResult, 'Selecciona primero una imagen con QR.', true);
                    return;
                }

                const reader = new FileReader();
                reader.onload = function (event) {
                    const img = new Image();
                    img.onload = function () {
                        const canvas = document.createElement('canvas');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0);
                        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                        const decoded = decodeQRFromImage(imageData);
                        if (decoded) {
                            showResult(fileResult, 'Contenido: ' + decoded);
                        } else {
                            showResult(fileResult, 'No se encontró ningún código QR en la imagen.', true);
                        }
                    };
                    img.src = event.target.result;
                };
                reader.readAsDataURL(file);
            }

            async function toggleCamera() {
                if (!cameraActive) {
                    await startCamera();
                } else {
                    stopCamera();
                }
            }

            async function startCamera() {
                try {
                    cameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
                    cameraVideo.srcObject = cameraStream;
                    await cameraVideo.play();
                    cameraActive = true;
                    photoState = 'take';
                    cameraActionBtn.textContent = 'Detener Cámara';
                    photoActionBtn.disabled = false;
                    photoActionBtn.textContent = 'Tomar Foto';
                    cameraVideo.style.display = 'block';
                    photoCanvas.style.display = 'none';
                    showResult(cameraResult, 'Cámara activada. Presiona Tomar Foto para capturar.');
                } catch (error) {
                    showResult(cameraResult, 'No se pudo iniciar la cámara: ' + error.message, true);
                }
            }

            function stopCamera() {
                stopCameraStream();
                cameraActive = false;
                photoState = 'none';
                cameraVideo.style.display = 'block';
                cameraActionBtn.textContent = 'Iniciar Cámara';
                photoActionBtn.disabled = true;
                photoActionBtn.textContent = 'Tomar Foto';
                photoCanvas.style.display = 'none';
                showResult(cameraResult, 'Cámara detenida.');
            }

            function stopCameraStream() {
                if (cameraStream) {
                    cameraStream.getTracks().forEach(track => track.stop());
                    cameraStream = null;
                }
                cameraVideo.pause();
                cameraVideo.srcObject = null;
            }

            function capturePhoto() {
                if (!cameraActive) {
                    showResult(cameraResult, 'Inicia primero la cámara.', true);
                    return;
                }

                const width = cameraVideo.videoWidth;
                const height = cameraVideo.videoHeight;
                if (!width || !height) {
                    showResult(cameraResult, 'La cámara aún no está lista. Intenta de nuevo.', true);
                    return;
                }

                photoCanvas.width = width;
                photoCanvas.height = height;
                const ctx = photoCanvas.getContext('2d');
                ctx.drawImage(cameraVideo, 0, 0, width, height);
                photoCanvas.style.display = 'block';
                cameraVideo.style.display = 'none';
                stopCameraStream();
                cameraActive = false;
                photoState = 'ready';
                cameraActionBtn.textContent = 'Iniciar Cámara';
                photoActionBtn.textContent = 'Obtener QR';
                showResult(cameraResult, 'Foto tomada. Presiona Obtener QR para leerla.');
            }

            function obtainQrFromPhoto() {
                const ctx = photoCanvas.getContext('2d');
                try {
                    const imageData = ctx.getImageData(0, 0, photoCanvas.width, photoCanvas.height);
                    const decoded = decodeQRFromImage(imageData);
                    if (decoded) {
                        showResult(cameraResult, 'Contenido: ' + decoded);
                    } else {
                        showResult(cameraResult, 'No se detectó QR en la foto.', true);
                    }
                } catch (error) {
                    showResult(cameraResult, 'Error al procesar la foto: ' + error.message, true);
                }
                photoState = 'reset';
                photoActionBtn.textContent = 'Tomar nueva foto';
            }

            function handlePhotoAction() {
                if (photoState === 'take') {
                    capturePhoto();
                } else if (photoState === 'ready') {
                    obtainQrFromPhoto();
                } else if (photoState === 'reset') {
                    photoActionBtn.textContent = 'Tomar Foto';
                    photoState = 'take';
                    cameraVideo.style.display = 'block';
                    photoCanvas.style.display = 'none';
                    showResult(cameraResult, 'Listo para tomar otra foto.');
                }
            }

            generateBtn.addEventListener('click', generateQRCode);
            downloadBtn.addEventListener('click', downloadQRCode);
            scanFileBtn.addEventListener('click', readFromFile);
            cameraActionBtn.addEventListener('click', toggleCamera);
            photoActionBtn.addEventListener('click', handlePhotoAction);
        </script>
    </body>
    </html>
    """
