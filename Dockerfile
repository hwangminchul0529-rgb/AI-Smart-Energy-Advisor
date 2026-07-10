FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["python","-m","streamlit","run","app.py","--server.port","8000","--server.address","0.0.0.0"]