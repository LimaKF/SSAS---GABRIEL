from flask import Flask
from models import db
from routes import api_routes  # Importa as rotas do outro arquivo
import os

app = Flask(__name__)

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://postgres:senha_secreta_123@db:5432/gateway_saas'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco
db.init_app(app)

# Registra as rotas
app.register_blueprint(api_routes)

# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)