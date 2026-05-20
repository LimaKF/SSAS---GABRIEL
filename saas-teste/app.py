from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    plano = data.get('plan')
    
    import time
    time.sleep(1) # Simulando o tempo de processamento
    
    if plano in ['basico', 'pro']:
        return jsonify({
            'status': 'success', 
            'message': f'Pagamento do plano {plano.upper()} aprovado com sucesso!',
            'redirect_url': '/sucesso'
        })
        
    return jsonify({'status': 'error', 'message': 'Plano inválido'}), 400

@app.route('/sucesso')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)