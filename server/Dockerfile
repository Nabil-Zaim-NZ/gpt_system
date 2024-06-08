FROM python:3.12.3-slim

ENV FLASK_APP=app.py
ENV ROOT /tmp/
ENV SERVER server/
ENV PYTHONPATH "${PYTHONPATH}:${ROOT}"

WORKDIR ${ROOT}/${SERVER}

ADD . ${ROOT}/${SERVER}
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["flask", "reindex"]

CMD ["flask", "run"]
