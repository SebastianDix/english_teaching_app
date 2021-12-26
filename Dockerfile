FROM python 

WORKDIR /

COPY package*.json ./

COPY . .

RUN pip install poetry
RUN poetry install 

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
