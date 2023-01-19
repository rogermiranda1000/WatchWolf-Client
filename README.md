# WatchWolf - MC Client
A Python library to test Minecraft Plugins in the client side.

## Dependencies
- [Docker](https://www.docker.com/get-started/)
- Python image: `docker pull nikolaik/python-nodejs`
- Build the image: `docker build --tag clients-manager .`

## Launch
- Run the docker container: `wsl_mode(){ echo "echo 'Hello world'" | powershell.exe >/dev/null 2>&1; return $?; } ; get_ip(){ wsl_mode; if [ $? -eq 0 ]; then echo "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Ethernet).IPAddress" | powershell.exe 2>/dev/null | tail -n2 | head -n1; else hostname -I | awk '{print $1}';fi } ; sudo docker run -i --rm --name ClientsManager -p 7000-7199:7000-7199 --env MACHINE_IP=$(get_ip) clients-manager:latest`