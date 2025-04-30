FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    libgbm1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.49/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.49/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/ && \
    cp -r /opt/chromedriver-linux64/* /opt/ && \
    cp -r /opt/chrome-linux64 /opt/chrome


# Adiciona variáveis de ambiente para Chrome em Docker
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Define diretório de trabalho
WORKDIR /src

ENV PYTHONPATH=/

# Copia o código
COPY . .

# Instala dependências Python
RUN pip install -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "src.automation.app:app", "--host", "0.0.0.0", "--port", "8000"]