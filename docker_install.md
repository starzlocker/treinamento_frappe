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

4. Instale o Docker seguindo as instruções em:
- [Instalação no Linux](https://docs.docker.com/desktop/setup/install/linux/)
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
    bench set-config -g redis_socketio redis://redis-queue:6379
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

