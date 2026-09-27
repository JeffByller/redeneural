import cv2
import mediapipe as mp
from flask import Flask, Response
import os

# --- 1. SETUP DO SERVIDOR WEB ---
app = Flask(__name__)

# --- 2. SETUP DA CÂMERA E DA IA ---
# Modifique aqui a URL da sua câmera (com senha)
RTSP_URL = 'rtsp://admin:@Jeff2712@10.64.0.61:554/'

# Inicializando os módulos de desenho, Mãos e Corpo do MediaPipe
mp_desenho = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

# Os parâmetros 'min_detection_confidence' regulam quão "certeza" a IA precisa ter
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# --- 3. A FUNÇÃO GERADORA DE VÍDEO (PIPELINE) ---
def gerar_frames():
    # Conecta na câmera
    cap = cv2.VideoCapture(RTSP_URL)
    
    print("Iniciando a transmissão RTSP -> IA -> Web Browser...")
    
    while True:
        # Lê um frame da câmera RTSP
        sucesso, frame = cap.read()
        if not sucesso:
            print("Falha ao ler o frame da câmera. Tentando novamente...")
            continue
            
        # O OpenCV lê em BGR (Azul, Verde, Vermelho). O MediaPipe precisa de RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Passa a imagem pela Rede Neural
        resultado_maos = hands.process(frame_rgb)
        resultado_corpo = pose.process(frame_rgb)
        
        # Desenha a teia das MÃOS na imagem original (que será mostrada ao usuário)
        if resultado_maos.multi_hand_landmarks:
            for mao in resultado_maos.multi_hand_landmarks:
                mp_desenho.draw_landmarks(frame, mao, mp_hands.HAND_CONNECTIONS)
                
        # Desenha o esqueleto do CORPO HUMANO na imagem original
        if resultado_corpo.pose_landmarks:
            mp_desenho.draw_landmarks(frame, resultado_corpo.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
        # --- O TRUQUE PARA A WEB (MJPEG) ---
        # Como o navegador HTML não sabe ler "Matrizes Python", precisamos 
        # converter de volta para uma imagem comprimida padrão (JPEG)
        ret, buffer_jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = buffer_jpeg.tobytes()
        
        # O 'yield' vai despejando os blocos da imagem de forma contínua no navegador
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# --- 4. AS ROTAS DO SERVIDOR ---
@app.route('/')
def index():
    # Uma página HTML super simples que renderiza o stream de vídeo ocupando a tela
    return """
    <html>
        <head>
            <title>Visão Computacional</title>
            <style>
                body { background-color: #1e1e1e; color: white; font-family: sans-serif; text-align: center; }
                img { max-width: 90%; max-height: 90vh; border: 3px solid #00ff00; border-radius: 10px; margin-top: 20px;}
            </style>
        </head>
        <body>
            <h2>IA : MediaPipe em Tempo Real</h2>
            <img src="/video_feed" />
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    # Retorna o fluxo infinito de imagens criado pela função 'gerar_frames'
    return Response(gerar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Roda o servidor na porta 5000 do nosso container
    print("Servidor no ar! Acesse no navegador: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
