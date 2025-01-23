FROM python:3.11
ADD reader.py .
ADD main.py .
RUN pip install discord
RUN pip install numpy
CMD ["python", "./main.py"]