# ** Projeto START.SE **

## ** Semana PYSTACKWEEK 11 (Ago/2024) **

# Para começar
* Crie um virtualenv

#### Windows

```bash 
python -m venv .venv
```

#### Linux

```bash
python3 -m venv .venv
```

* Ative o virtualenv
#### Windows
```bash
 .venv/Scripts/activate
 ```

#### Linux
```bash
source .venv/bin/activate
```

OBS: À partir de agora que acessou a virtualenv todos os comandos dentro dela só precisa usar **python e pip**

* Instale as dependências.

```bash
pip install -r requirements.txt
```

* Rode as migrações.

```bash
python manage.py migrate
```

* Crie um usuário

```bash
python manage.py createsuperuser
```

* Rode a aplicação

```bash
python manage.py runserver
```