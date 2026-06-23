from flask import Blueprint, request, jsonify, render_template
from models import db, Lojista, Cliente, Transacao

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/')
def index():
    # Renderiza a página principal do Checkout
    return render_template('index.html')

@api_routes.route('/api/checkout', methods=['POST'])
def checkout():
    # 1. Autenticação via Header
    api_token = request.headers.get('Authorization')
    if not api_token:
        return jsonify({'status': 'error', 'message': 'Token de API não fornecido.'}), 401
        
    token_limpo = api_token.replace('Bearer ', '') if 'Bearer ' in api_token else api_token
    lojista = Lojista.query.filter_by(api_token=token_limpo).first()
    if not lojista:
        return jsonify({'status': 'error', 'message': 'Token de API inválido.'}), 401

    # 2. Dados da Requisição
    data = request.json or {}
    plano = data.get('plan', 'Plano Premium')
    valor = data.get('valor', 99.90)
    metodo = data.get('metodo_pagamento', 'pix')
    
    # 3. Cliente de Teste
    cliente = Cliente.query.filter_by(email='comprador@teste.com').first()
    if not cliente:
        cliente = Cliente(nome='Comprador Teste', documento='12345678909', email='comprador@teste.com')
        db.session.add(cliente)
        db.session.commit()

    # No mundo real, PIX nasce como 'pendente'. Cartão pode ser aprovado direto.
    status_inicial = 'pendente' if metodo == 'pix' else 'aprovado'

    # 4. Salva a transação no banco
    nova_transacao = Transacao(
        lojista_id=lojista.id,
        cliente_id=cliente.id,
        valor=valor,
        status=status_inicial,
        metodo_pagamento=metodo
    )
    db.session.add(nova_transacao)
    db.session.commit()

    # 5. Resposta Estruturada para o Frontend
    resposta = {
        'status': 'success',
        'transaction_id': nova_transacao.id,
        'metodo_pagamento': metodo,
        'valor': float(valor)
    }

    if metodo == 'pix':
        # Simulando exatamente o payload que o Asaas ou Mercado Pago devolveriam
        resposta.update({
            'pix_copia_e_cola': '00020101021126580014br.gov.bcb.pix0136c4583adb36574ab2a3e27be747bf8ce9520400005303986540599.905802BR5924Nosso Gateway SaaS6009Sao Paulo62070503***6304A1B2',
            # Usando uma API pública para gerar um QR code visual a partir da string acima
            'qr_code_url': f'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=00020101021126580014br.gov.bcb.pix'
        })
    else:
        resposta.update({
            'redirect_url': '/sucesso'
        })

    return jsonify(resposta)

@api_routes.route('/sucesso')
def success():
    return render_template('success.html')