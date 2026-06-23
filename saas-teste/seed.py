from app import app
from models import db, Lojista
from werkzeug.security import generate_password_hash

def popular_banco():
    with app.app_context():
        # Verifica se o lojista já existe para não criar duplicado
        lojista_existente = Lojista.query.filter_by(email='admin@nosso-saas.com').first()
        
        if not lojista_existente:
            novo_lojista = Lojista(
                nome='Lojista Parceiro (Teste)',
                email='admin@nosso-saas.com',
                senha_hash=generate_password_hash('senha_segura_123')
            )
            db.session.add(novo_lojista)
            db.session.commit()
            
            print("✅ Lojista criado com sucesso!")
            print(f"🆔 ID: {novo_lojista.id}")
            print(f"🔑 Token da API: {novo_lojista.api_token}")
        else:
            print("⚠️ O lojista de teste já existe no banco de dados.")
            print(f"🔑 Token da API: {lojista_existente.api_token}")

if __name__ == '__main__':
    popular_banco()