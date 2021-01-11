# Candidatos2020
Busca os resultados por urna do primeiro turno dos candidados

# Criando o ambiente virtual
virtualenv venv

# Habilitando o ambiente Windows
source venv/Scripts/activate

# Habilitando o ambiente linux
source venv/bin/activate

# Com o ambiente habilitado instalar as dependências.
pip install -r requirements.txt 

# Entrar no diretório do site
cd mysite

# Iniciando o banco de dados sqllite3
python manage.py migrate

# Criando o super usuário para usar as funções de admin
python manage.py createsuperuser

# Iniciando o site
python manage.py runserver

