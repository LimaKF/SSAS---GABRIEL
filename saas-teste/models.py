from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Lojista(db.Model):
    __tablename__ = 'lojistas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    api_token = db.Column(db.String(64), unique=True, default=lambda: uuid.uuid4().hex)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento: Um lojista pode ter várias transações
    transacoes = db.relationship('Transacao', backref='lojista', lazy=True)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)  # CPF ou CNPJ
    email = db.Column(db.String(120), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class Transacao(db.Model):
    __tablename__ = 'transacoes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lojista_id = db.Column(db.Integer, db.ForeignKey('lojistas.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pendente')  # pendente, aprovado, recusado, estornado
    metodo_pagamento = db.Column(db.String(20), nullable=False)  # pix, cartao
    
    # Campo para armazenar o ID gerado pela processadora externa final (Asaas, Mercado Pago, etc.)
    provedor_externo_id = db.Column(db.String(100), nullable=True)
    
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)