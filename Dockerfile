FROM python:3.12-alpine

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /bot

COPY bot.py commands.py routing.py secrets.env db_password.txt ./

COPY db/ db/
COPY item/ item/
COPY keyboards/ keyboards/
COPY handlers/ handlers/

CMD ["python", "bot.py"]
