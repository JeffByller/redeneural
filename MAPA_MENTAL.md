# 🧠 Mapa Mental: Laboratório de Visão Computacional e IA

Este diagrama resume toda a nossa jornada técnica desconstruindo como o computador enxerga o mundo, desde a captura dos pacotes de rede até o processamento geométrico feito por Redes Neurais Profundas (Deep Learning).

```mermaid
flowchart LR
    ROOT(("🤖 Visão Computacional\n& Redes Neurais"))
    
    %% Ramo 1: A Imagem
    ROOT --> IMG["🖼️ 1. A Natureza da Imagem"]
    IMG --> MAT["Matrizes (Tabelas de Números)"]
    IMG --> COR["Canais de Cor (RGB, BGR)"]
    IMG --> ROI["Slicing / Recorte (Region of Interest)"]

    %% Ramo 2: Redes e Protocolos
    ROOT --> REDE["📡 2. Transporte de Vídeo (Rede)"]
    REDE --> RTSP["Protocolo RTSP"]
    RTSP --> TCP["TCP: Controle e Autenticação (Porta 554)"]
    RTSP --> UDP["UDP / RTP: Despejo Massivo de Frames"]
    REDE --> SNIF["Análise de Pacotes (TCPDump / Wireshark)"]

    %% Ramo 3: Processamento Clássico
    ROOT --> CLASSIC["⚙️ 3. Visão Clássica (Pré-IA)"]
    CLASSIC --> CINZ["Conversão Escala de Cinza (Otimização)"]
    CLASSIC --> CANNY["Filtro Canny (Extração de Bordas)"]
    CLASSIC --> CONT["Identificação baseada em Contraste de Luz"]

    %% Ramo 4: Inteligência Artificial
    ROOT --> IA["🧠 4. Deep Learning (IA)"]
    IA --> PIPE["Pipeline de Múltiplas Redes"]
    PIPE --> DET["Rede 1 (Detector): Encontra o Objeto"]
    PIPE --> LAND["Rede 2 (Regressor): Extrai Coordenadas"]
    IA --> RAW["A Verdadeira Saída da IA"]
    RAW --> XYZ["Números Geométricos: Posições X, Y, Z"]
    RAW --> GEST["Gestos são cálculos matemáticos (Ex: Pitágoras)"]

    %% Ramo 5: Performance
    ROOT --> PERF["⚡ 5. Engenharia de Performance"]
    PERF --> GARG["Gargalo: Renderizar imagem por imagem no Frontend"]
    PERF --> DISCO["Solução A: Gravação direta em Disco (VideoWriter)"]
    PERF --> WEB["Solução B: Servidor de Streaming (MJPEG via Flask)"]
```

---

### Resumo dos Principais Pontos sobre Redes Neurais (MediaPipe)
Se alguém te perguntar *"Como o MediaPipe da Google funciona no código que você fez?"*, aqui está a resposta definitiva:

> [!NOTE] 
> **A IA não "pinta" a tela, ela faz cálculos geométricos.**
> A rede neural é um modelo treinado em milhões de fotos. Quando você manda um frame para ela, ela não te devolve uma imagem com linhas verdes desenhadas. Ela retorna um documento cheio de **Coordenadas Matemáticas**. Todo o trabalho de desenhar as linhas (Computação Gráfica) ou calcular distâncias para saber se você fez um gesto de pinça é feito por algoritmos paralelos usando os dados puros que a IA encontrou.

> [!TIP]
> **O truque do Pipeline.**
> Redes neurais pesadas travam PCs comuns. A Google resolveu isso quebrando a rede ao meio. A primeira rede procura apenas onde o alvo está (sua mão). Assim, a segunda rede neural (muito mais inteligente e pesada) só precisa olhar para uma fração minúscula da imagem, calculando o esqueleto (Landmarks) quase instantaneamente.
