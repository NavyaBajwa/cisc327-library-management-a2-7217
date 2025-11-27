FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Set working directory in the container
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Now copy all your source files into the container
COPY . /app

# Expose the port Flask uses
EXPOSE 5000

# Run the server
CMD ["flask", "run"]
