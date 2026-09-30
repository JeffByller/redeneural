import cv2
import mediapipe as mp
import time
import os

# Coloque a sua URL com senha aqui!
RTSP_URL = 'rtsp://admin:@Jeff2712@10.64.0.60:554/'

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(RTSP_URL)

print("Iniciando captura... Prepare-se para ver os dados brutos da IA!")
time.sleep(2)

try:
    while True:
        inicio = time.time()
        ret, frame = cap.read()
        if not ret:
            print("Tentando reconectar...")
            time.sleep(1)
            continue
            
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # --- A INFERÊNCIA (O processamento real da Rede Neural) ---
        resultado = hands.process(frame_rgb)
        
        tempo_processamento = (time.time() - inicio) * 1000 # Em milissegundos
        
        # Limpa o terminal para criar efeito de "Painel de Controle / Matrix"
        os.system('clear')
        
        print("=========================================")
        print("  MOTOR DE INFERÊNCIA MEDIAPIPE (RAW)")
        print("=========================================")
        print(f"Velocidade do cérebro : {tempo_processamento:.2f} ms por frame")
        print("-----------------------------------------\n")
        
        if resultado.multi_hand_landmarks:
            print("[ STATUS ] >>> MÃO HUMANA DETECTADA!\n")
            
            for id_mao, mao in enumerate(resultado.multi_hand_landmarks):
                # O MediaPipe mapeia 21 pontos. Vamos extrair o Ponto 8 (Ponta do Indicador)
                indicador = mao.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                polegar = mao.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                print(f"--- DETECÇÃO {id_mao + 1} ---")
                print(f" PONTA INDICADOR -> X: {indicador.x:.4f} | Y: {indicador.y:.4f} | Profundidade(Z): {indicador.z:.4f}")
                print(f" PONTA POLEGAR   -> X: {polegar.x:.4f} | Y: {polegar.y:.4f} | Profundidade(Z): {polegar.z:.4f}")
                
                # Logica matemática simples baseada nos dados puros:
                distancia_y = indicador.y - polegar.y
                if distancia_y > 0:
                    print("\n LÓGICA: O indicador está abaixo do polegar.")
                else:
                    print("\n LÓGICA: O indicador está acima do polegar.")
                
                print("\n")
        else:
            print("[ STATUS ] : Nenhuma mão detectada. Visão limpa.")
            print("Aguardando alvo...")
            
except KeyboardInterrupt:
    print("\nEncerrando o modo Matrix...")
finally:
    cap.release()
