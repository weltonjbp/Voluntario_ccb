from flask import Blueprint, render_template

# Cria um Blueprint para rotas gerais
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    return render_template('index.html')