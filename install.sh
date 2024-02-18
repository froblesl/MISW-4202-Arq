# No es necesario en macOS
# sudo apt update

# Instalar Docker Desktop para Mac desde el sitio web oficial de Docker: https://www.docker.com/products/docker-desktop

# No es necesario en macOS
# sudo apt install docker.io

# No es necesario en macOS
# sudo usermod -aG docker $USER

# Instalar Docker Compose utilizando Homebrew
brew install docker-compose

# Descargar Docker Compose y dar permisos de ejecución
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
