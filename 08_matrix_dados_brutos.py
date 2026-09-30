import cv2
import mediapipe as mp
import time
from flask import Flask, Response, jsonify
import os

app = Flask(__name__)

RTSP_URL = 'rtsp://admin:@Jeff2712@10.64.0.60:554/'

mp_hands = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variável global para guardar os últimos dados lidos
dados_matrix = {
    "status": "Aguardando alvo...",
    "tempo_processamento": 0,
    "maos": []
}

def gerar_frames():
    global dados_matrix
    cap = cv2.VideoCapture(RTSP_URL)
    
    while True:
        inicio = time.time()
        sucesso, frame = cap.read()
        if not sucesso:
            time.sleep(1)
            continue
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = hands.process(frame_rgb)
        
        tempo_processamento = (time.time() - inicio) * 1000
        
        # Resetando os dados para esse frame
        maos_detectadas = []
        status_atual = "Visão limpa."
        
        if resultado.multi_hand_landmarks:
            status_atual = "MÃO HUMANA DETECTADA!"
            for id_mao, mao in enumerate(resultado.multi_hand_landmarks):
                # Desenha os pontos na imagem
                mp_desenho.draw_landmarks(frame, mao, mp_hands.HAND_CONNECTIONS)
                
                indicador = mao.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                polegar = mao.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                posicao = "abaixo" if indicador.y > polegar.y else "acima"
                
                maos_detectadas.append({
                    "id": id_mao + 1,
                    "ind_x": round(indicador.x, 4),
                    "ind_y": round(indicador.y, 4),
                    "pol_x": round(polegar.x, 4),
                    "pol_y": round(polegar.y, 4),
                    "logica": f"Indicador está {posicao} do polegar"
                })

        dados_matrix["status"] = status_atual
        dados_matrix["tempo_processamento"] = round(tempo_processamento, 2)
        dados_matrix["maos"] = maos_detectadas
        
        # Converter imagem para JPG
        ret, buffer_jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = buffer_jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Matrix - Dados Brutos + Video</title>
            <style>
                body { background-color: #0d0d0d; color: #00ff00; font-family: monospace; display: flex; padding: 20px; }
                #video-container { flex: 2; text-align: center; }
                #video-container img { max-width: 100%; border: 2px solid #00ff00; border-radius: 8px; }
                #console-container { flex: 1; margin-left: 20px; background: #000; padding: 20px; border: 1px solid #00ff00; height: 80vh; overflow-y: auto; }
                h1, h2 { color: #00ff00; text-shadow: 0 0 5px #00ff00; }
                .linha { margin-bottom: 10px; border-bottom: 1px dashed #004400; padding-bottom: 10px;}
            </style>
        </head>
        <body>
            <div id="video-container">
                <h1>Matrix + Visão</h1>
                <img src="/video_feed" />
            </div>
            <div id="console-container">
                <h2>Dados Brutos (Raw)</h2>
                <div id="conteudo">Conectando ao terminal...</div>
            </div>

            <script>
                function atualizarDados() {
                    fetch('/dados')
                    .then(response => response.json())
                    .then(data => {
                        let html = `<div class="linha">
                            <b>Status:</b> ${data.status}<br>
                            <b>Velocidade:</b> ${data.tempo_processamento} ms
                        </div>`;
                        
                        data.maos.forEach(mao => {
                            html += `<div class="linha">
                                <b>>>> DETECÇÃO ${mao.id}</b><br>
                                INDICADOR: X:${mao.ind_x} | Y:${mao.ind_y}<br>
                                POLEGAR: X:${mao.pol_x} | Y:${mao.pol_y}<br>
                                <span style="color: #ffaa00;">-> LÓGICA: ${mao.logica}</span>
                            </div>`;
                        });
                        
                        document.getElementById('conteudo').innerHTML = html;
                    });
                }
                
                // Atualiza o painel lateral a cada 100 milissegundos
                setInterval(atualizarDados, 100);
            </script>
        </body>
    </html>
    """

@app.route('/video_feed')
def video_feed():
    return Response(gerar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dados')
def dados():
    return jsonify(dados_matrix)

if __name__ == '__main__':
    print("Modo Matrix Web ativado! Acesse http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
