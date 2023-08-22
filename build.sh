docker build -t secure_terminal .
docker run -d --restart unless-stopped -p 8045:8045 --name=secure_terminal secure_terminal
