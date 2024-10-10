FROM python:3.12-alpine3.19

LABEL authors="smiley-94"
LABEL project="Keysmith"

COPY . .

RUN python3 -m venv /venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt

RUN chmod +x run.sh

CMD ["sh", "run.sh"]



