# psie-kernel v4 — imagine suverană: nucleul determinist + Matricea Conștientă (server.py)
FROM python:3.12-slim
WORKDIR /app

# Nucleul: zero dependente — instalat ca pachet
COPY pyproject.toml README.md ./
COPY psie_kernel ./psie_kernel
RUN pip install --no-cache-dir .

# Straturile de serviciu: FastAPI + uvicorn
COPY requirements.txt server.py ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
