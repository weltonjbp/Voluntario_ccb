from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    estado_civil = db.Column(db.String(30))
    renda_mensal = db.Column(db.Float, nullable=False)
    logradouro = db.Column(db.String(80))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(20))
    estado = db.Column(db.String(15))
    cidade = db.Column(db.String(60), index=True)
    whatsapp = db.Column(db.String(20))
    telefone = db.Column(db.String(20))  # Adicionado conforme SQL

    __table_args__ = (
        CheckConstraint("renda_mensal >= 0", name="renda_mensal_positive"),
    )

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    mesa = db.Column(db.Integer)
    data = db.Column(db.Date)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    __table_args__ = (
        CheckConstraint("preco >= 0", name="preco_positive"),
    )

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    observacoes = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        CheckConstraint("quantidade > 0", name="quantidade_positive"),
    )

class Venda(db.Model):
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.DateTime)
    total = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint("total >= 0", name="total_positive"),
    )