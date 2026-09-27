FROM python:3.10-slim

WORKDIR /app

# Instala as dependências de sistema necessárias para o OpenCV, manipulação de vídeo (ffmpeg) e processamento
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as bibliotecas Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Jupyter Lab
EXPOSE 8888

# Inicia o Jupyter Lab (acessível no navegador)
CMD ["jupyter", "lab", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token='cvlab'", "--NotebookApp.password=''"]
