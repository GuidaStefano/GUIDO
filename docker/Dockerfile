# Usa Ubuntu 20.04 come base
FROM ubuntu:20.04

# Imposta il frontend non interattivo per evitare prompt durante il build
ARG DEBIAN_FRONTEND=noninteractive

# --- 1. INSTALLAZIONE DELLE DIPENDENZE DI SISTEMA ---
# Combina le installazioni in un unico layer per ottimizzare la dimensione dell'immagine
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Dipendenze di build essenziali
    build-essential \
    # Per aggiungere PPA esterni (deadsnakes)
    software-properties-common \
    # Dipendenze per librerie Python comuni (es. Matplotlib)
    libfreetype6-dev \
    libpng-dev \
    # Altri strumenti
    git \
    openjdk-8-jdk \
    && add-apt-repository ppa:deadsnakes/ppa && \
    # Installa entrambe le versioni di Python e i loro pacchetti -dev e -venv
    apt-get update && \
    apt-get install -y python3.8 python3.8-dev python3.8-venv \
    python3.11 python3.11-dev python3.11-venv && \
    # Pulisci la cache di apt per ridurre la dimensione dell'immagine
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Imposta l'ambiente per Matplotlib (se necessario)
ENV MPLLOCALFREETYPE=1

# Imposta l'ambiente per Java
ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
# Nota: git e java sono già nel PATH di sistema, non è necessario aggiungerli manualmente

# --- 2. PREPARAZIONE DELL'APPLICAZIONE ---
RUN mkdir /app
WORKDIR /app

# --- 3. CREAZIONE DI DUE AMBIENTI VIRTUALI SEPARATI ---
# Non modifichiamo il PATH globale per evitare ambiguità.
# Creiamo un ambiente virtuale per ogni versione di Python.
RUN python3.8 -m venv /opt/venv3.8
RUN python3.11 -m venv /opt/venv3.11

# --- 4. CLONAZIONE DEI REPOSITORY ---
# Clona il progetto principale e i sottoprogetti direttamente nella work directory
RUN git clone https://github.com/benedettoscala/csDetector.git .
RUN git clone https://github.com/FrancescoTorino1999/GUIDO.git
RUN git clone https://github.com/leotodisco/culture-inspector.git
RUN git clone https://github.com/GuidaStefano/TOAD.git

# --- 5. INSTALLAZIONE DELLE DIPENDENZE PYTHON NEI RISPETTIVI AMBIENTI ---
# Aggiorna pip, setuptools e wheel in entrambi gli ambienti come buona pratica
RUN /opt/venv3.8/bin/python -m pip install --upgrade pip setuptools wheel
RUN /opt/venv3.11/bin/python -m pip install --upgrade pip setuptools wheel

# Installa i requirements specificando l'interprete del venv corretto
RUN /opt/venv3.11/bin/python -m pip install -r TOAD/requirements.txt
RUN /opt/venv3.8/bin/python -m pip install -r GUIDO/requirements.txt
RUN /opt/venv3.8/bin/python -m pip install -r culture-inspector/requirements.txt
RUN /opt/venv3.8/bin/python -m pip install -r requirements.txt

# --- 6. INSTALLAZIONE PACCHETTI AGGIUNTIVI E DOWNLOAD ---
# Installa spacy e scarica il modello nell'ambiente Python 3.8
RUN /opt/venv3.8/bin/python -m pip install spacy
RUN /opt/venv3.8/bin/python -m spacy download en_core_web_sm

# Scarica i dati di NLTK usando l'ambiente Python 3.8
# Usiamo un pipe per essere più puliti, invece di creare un file temporaneo
RUN echo "import nltk; nltk.download('punkt')" | /opt/venv3.8/bin/python

# --- 7. CONFIGURAZIONE FINALE E RUNTIME ---
# Imposta le variabili d'ambiente per il runtime
ENV PAT=''
ENV CLIENT_ID="f5fc77806e10b7e7d5f0"
ENV SIMILARITY_MAX_DISTANCE=0.4
ENV CSDETECTOR_URL_GETSMELLS='http://127.0.0.1:5001/getSmells'
ENV GEODISPERSION_URL='http://127.0.0.1:5004/compute_std_dev'
ENV TOAD_URL = 'http://127.0.0.1:8000'

# Copia lo script di avvio nel container
COPY ./run.sh /app/run.sh

# Rende lo script eseguibile
RUN chmod +x /app/run.sh

# Espone la porta per l'applicazione
EXPOSE 5005

# Esegue lo script quando il container viene avviato
CMD ["/app/run.sh"]