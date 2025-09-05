@app.route("/funcionarios", methods=["POST"])
def criar_funcionario():
    data = request.json
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Nome é obrigatório"}), 400

    funcionario = Funcionario(nome=nome)
    db.session.add(funcionario)
    db.session.commit()

    return jsonify({"id": funcionario.id, "nome": funcionario.nome}), 201


# Registrar ponto
@app.route("/ponto", methods=["POST"])
def registrar_ponto():
    data = request.json
    funcionario_id = data.get("funcionario_id")
    tipo = data.get("tipo")

    if tipo not in ["entrada", "saida"]:
        return jsonify({"erro": "Tipo deve ser 'entrada' ou 'saida'"}), 400

    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    registro = RegistroPonto(funcionario_id=funcionario.id, tipo=tipo)
    db.session.add(registro)
    db.session.commit()

    return jsonify({
        "id": registro.id,
        "funcionario": funcionario.nome,
        "tipo": registro.tipo,
        "timestamp": registro.timestamp.isoformat()
    }), 201


# Listar registros de um funcionário
@app.route("/ponto/<int:funcionario_id>", methods=["GET"])
def listar_pontos(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    registros = [
        {"id": r.id, "tipo": r.tipo, "timestamp": r.timestamp.isoformat()}
        for r in funcionario.registros
    ]

    return jsonify({"funcionario": funcionario.nome, "registros": registros})