# Use Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for caching dependencies)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot's files
COPY . .

# Expose the necessary port (if applicable, usually not needed for a bot)
# EXPOSE 8080 

# Run the bot with environment variables
CMD ["python", "run_bot.py"]
