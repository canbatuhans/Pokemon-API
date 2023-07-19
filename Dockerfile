# Base image
FROM python:3.9

# Uygulama klasörünü oluşturma
RUN mkdir /app
WORKDIR /app

# Gerekli dosyaları kopyalama
COPY requirements.txt /app
COPY api.py /app

# Bağımlılıkları yükleme
RUN pip install --no-cache-dir -r requirements.txt

# Portu belirtme
EXPOSE 5000

# Uygulama çalıştırma komutu
CMD ["python", "api.py"]

