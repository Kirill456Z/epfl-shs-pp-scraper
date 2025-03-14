FROM mcr.microsoft.com/playwright:v1.50.0-noble

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# Install packages without checking hashes
RUN pip install --no-cache-dir --no-deps --ignore-installed -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0"]
