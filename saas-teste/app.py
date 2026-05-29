from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SERVICOS = {
    'tarot_simples': {
        'nome': 'Tiragem de Tarot Simples',
        'preco': 40.00
    },
    'tarot_completa': {
        'nome': 'Tiragem de Tarot Completa',
        'preco': 99.90
    },
    'limpeza': {
        'nome': 'Limpeza Energética',
        'preco': 149.90
    },
    'consulta': {
        'nome': 'Consulta Completa',
        'preco': 239.90
    },
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    plano = data.get('plan')

    import time
    time.sleep(1)  # Simulando tempo de processamento

    if plano in SERVICOS:
        servico = SERVICOS[plano]
        return jsonify({
            'status': 'success',
            'message': f'Pagamento de "{servico["nome"]}" aprovado com sucesso!',
            'redirect_url': '/sucesso'
        })

    return jsonify({'status': 'error', 'message': 'Serviço inválido'}), 400

@app.route('/sucesso')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)