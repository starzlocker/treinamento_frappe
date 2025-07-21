# Instruções para configuração de ambiente de desenvolvimento de frappe com Docker

## Clonando o projeto frappe_docker

1. Inicie o VSCode e abra a pasta onde deseja clonar o projeto:
    ```sh
    git clone https://github.com/frappe/frappe_docker.git
    cd frappe_docker
    ```

2. Copie os exemplos de configuração:
    ```sh
    cp -R devcontainer-example .devcontainer
    cp -R development/vscode-example development/.vscode
    ```

3. Instale a extensão do VS Code para containers remotos:
    ```sh
    code --install-extension ms-vscode-remote.remote-containers
    ```

4. Instruções completas no link:
- [Instalação no Linux](https://docs.docker.com/desktop/setup/install/linux/)

# Instalação do Docker no Linux
4.0 Rode no terminal

``` bash
sudo apt install gnome-terminal
```

4.1 Baixe o pacote .deb [Pacote](https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64&_gl=1*ri1xc9*_ga*MTk5MzU2MTI2LjE3NDkwNjE1NTA.*_ga_XJWPQMJYHQ*czE3NTMxMTIyNjAkbzQkZzEkdDE3NTMxMTIyNjMkajU3JGwwJGgw)

4.2 Baixe o repositório do Docker
``` bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

4.3 Rode os seguintes comandos

``` bash
sudo apt-get update
# Rode o arquivo que vc baixou
sudo apt-get install ./docker-desktop-amd64.deb
```

4.4 O erro abaixo é esperado, pode ignorar
``` bash
N: Download is performed unsandboxed as root, as file '/home/user/Downloads/docker-desktop.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```

- [Instalação no Windows](https://docs.docker.com/desktop/setup/install/windows-install/)



5. No terminal, dentro da pasta `frappe_docker`, inicie o VSCode.
    ```sh
    code .
    ```

6. Use o atalho `CTRL + SHIFT + P` e pesquise por "Dev Containers: Reopen in Container".

## Configuração do Bench

1. Abra outro terminal e inicialize o Bench:
    ```sh
    bench init --skip-redis-config-generation frappe-bench
    cd frappe-bench
    ```

2. Configure o banco de dados e o Redis:
    ```sh
    bench set-config -g db_host mariadb
    bench set-config -g redis_cache redis://redis-cache:6379
    bench set-config -g redis_queue redis://redis-queue:6379
    bench set-config -g redis_socketio redis://redis_socketio:6379
    ```

3. Crie um novo site:
    ```sh
    bench new-site --mariadb-root-password 123 --admin-password admin --no-mariadb-socket development.localhost
    ```
- `--mariadb-root-password 123`: Define a senha root do MariaDB como `123`.
- `--admin-password admin`: Define a senha do administrador do site como `admin`.
- `--no-mariadb-socket`: Indica que não será utilizado o socket do MariaDB.
- `development.localhost`: Nome do site que está sendo criado.

4. Defina o site como padrão:
    ```sh
    bench use development.localhost
    ```

5. Inicie o Bench:
    ```sh
    bench start
    ```

6. Acesse o [site](http://0.0.0.0:8000/) e utilize:
    - **Usuário**: `administrator`
    - **Senha**: `admin`

