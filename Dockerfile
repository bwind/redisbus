FROM python:3.7

RUN echo "alias l='ls -lahF --color=auto'" >> /root/.bashrc
RUN echo "python -m pytest -x" >> /root/.bash_history

WORKDIR /app

COPY requirements*.txt /app/

RUN pip install -r requirements.txt
