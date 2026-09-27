# 📷 Laboratório de Visão Computacional: Roadmap de Estudos

Bem-vindo ao seu laboratório pessoal de Visão Computacional! O foco deste laboratório é **aprender**, desconstruir o funcionamento das coisas e aplicar conceitos de visão computacional na prática, usando a câmera IP local (`10.64.0.61`).

Usaremos **Jupyter Notebooks** rodando no Docker para que você possa executar blocos de código de forma interativa, testando filtros, vendo os resultados passo a passo e entendendo o "porquê" de cada linha.

---

## 🗺️ Fases do Laboratório

### **Fase 1: Fundamentos e Captura de Vídeo**
*O objetivo inicial é estabelecer comunicação com a câmera e entender como as imagens são representadas no computador (Matrizes).*

1. **Captura do RTSP com OpenCV:** Como abrir um stream contínuo, ler os frames e salvar o último frame como imagem.
2. **Entendendo a Imagem (Pixels e Matrizes):** Como o NumPy lida com os arrays de imagem. Inspeção de dimensões (Altura, Largura, Canais de Cor).
3. **Conversão de Espaços de Cor:** Explorar BGR (padrão do OpenCV) vs RGB vs Escala de Cinza vs HSV. Por que usar HSV é melhor para identificar cores em iluminação variável?

### **Fase 2: Processamento Clássico de Imagens**
*Antes de partirmos para Inteligência Artificial, precisamos entender a manipulação de imagens.*

1. **Suavização e Blurring:** Filtros Gaussianos, Filtro de Mediana. O que é "ruído" na imagem e como removê-lo.
2. **Detecção de Bordas (Canny Edge Detection):** Como o computador percebe contrastes para achar o contorno dos objetos.
3. **Thresholding (Binarização):** Técnicas para transformar a imagem em Preto e Branco baseadas na intensidade da luz.
4. **Morfologia Matemática:** Erosão e Dilatação (para "limpar" buracos nas máscaras).

### **Fase 3: Detecção e Rastreamento (Sem Deep Learning)**
*Criando lógicas de vigilância e sensoriamento.*

1. **Subtração de Fundo (Background Subtraction):** Como o computador sabe que algo se mexeu? (Algoritmos KNN ou MOG2).
2. **Detecção de Movimento:** Desenhando _Bounding Boxes_ (caixas retangulares) sobre áreas que estão se movendo na câmera da bancada.
3. **Identificação de Cores:** Criando um "rastreador de objetos coloridos" (ex: rastrear uma tampa de caneta vermelha que você passa na frente da câmera).

### **Fase 4: Deep Learning & Inteligência Artificial**
*Onde a mágica moderna acontece: ensinando o computador a identificar 'o que' são as coisas.*

1. **MediaPipe (Google):** 
   - Rastreamento de Mãos e Dedos na frente da câmera.
   - Detecção de Rosto e Pontos Faciais.
2. **YOLOv8 (Ultralytics):**
   - Detecção de objetos em tempo real (Pessoas, Celulares, Copos).
   - O que é _Confidence Score_ (Nível de confiança) e _Non-Maximum Suppression_ (NMS)?

### **Fase 5: Mini-Projetos de Fixação (Aplicações Práticas)**
*Unindo tudo que aprendemos para criar ferramentas funcionais.*

1. **Alarme de Invasão de Perímetro:** Você desenha uma "zona virtual" no frame. Se a câmera detectar movimento dentro dela, salva uma foto na pasta e emite um alerta no log.
2. **Contador de Objetos:** Passar objetos numa direção específica da bancada e contar (ex: da esquerda para a direita aumenta +1).
3. **Controle por Gesto:** Ligar uma variável no código fazendo "sinal de positivo 👍" para a câmera.

---

## 🛠️ Como usar este laboratório?

Todo o ambiente está conteinerizado no Docker. Para começar a brincar:

1. Suba os containers: `docker-compose up -d --build`
2. Acesse o ambiente Jupyter no seu navegador através do endereço:
   👉 **http://localhost:8888**
   👉 **Token de acesso:** `cvlab`
3. Crie Notebooks (`.ipynb`) dentro do Jupyter para cada fase do seu roadmap e experimente o código.
