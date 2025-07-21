Instalando o frappe no docker

``` bash
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker 

cp -R devcontainer-example .devcontainer & 
cp -R development/vscode-example
development/.vscode

code --install-extension ms-vscode-remote.remote-containers 

bench init --skip-redis-config-generation frappe-bench 

cd frappe-bench 


bench set-config -g db_host mariadb &
bench set-config -g redis_cache redis://redis_cache:6379 & 
bench set-config -g redis_queue redis://redis_queue:6379 &
bench set-config -g redis_socketio redis://redis_socketio:6379

bench new-site --mariadb-root-password 123 --admin-password admin --no-mariadb-socket
development.localhost 

bench new-app treino

bench use treino.localhost

bench start

nvm install 18.18.2

``