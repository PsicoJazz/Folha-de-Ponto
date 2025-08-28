from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuração correta do PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qweqwe@localhost:5432/registro_ponto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela
class RegistroPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    entrada = db.Column(db.Time, nullable=True)
    saida = db.Column(db.Time, nullable=True)

    def __repr__(self):
        return f'<RegistroPonto {self.nome} - {self.data}>'

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        agora = datetime.now()
        data = agora.date()
        hora = agora.time()

        if tipo == 'entrada':
            registro = RegistroPonto(nome=nome, data=data, entrada=hora)
            db.session.add(registro)
        elif tipo == 'saida':
            registro = RegistroPonto.query.filter_by(nome=nome, data=data, saida=None).order_by(RegistroPonto.id.desc()).first()
            if registro:
                registro.saida = hora

        db.session.commit()
        return redirect(url_for('index'))

    registros = RegistroPonto.query.order_by(RegistroPonto.data.desc(), RegistroPonto.nome).all()
    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
