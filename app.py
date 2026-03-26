from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'Qualquer coisa'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resultados')
def resultados():
    calculos = session.get('calculos', [])

    return render_template('resultados.html', calculos=calculos, total=len(calculos))


@app.route('/calcular', methods=['GET', 'POST'])
def calcular():

    if request.method == 'POST':
        nome = request.form.get('nome', 'Não, achei porra nenhuma')
        peso = request.form.get('peso', '0')
        altura = request.form.get('altura', '0')

        imc = round(float(peso) / (float(altura) ** 2), 2)
        
        if imc < 18.5:
            classificacao = 'Abaixo do peso'

        elif imc < 25:
            classificacao = 'Peso normal'

        elif imc < 30:
            classificacao = 'Sobrepeso'

        elif imc < 35.0:
            classificacao = 'Obesidade grau I'

        elif imc < 40.0:
            classificacao = 'Obesidade grau II'

        elif imc >= 40.0:
            classificacao = 'Obesidade grau III'

        else:
            classificacao = 'Deu erro na conta!'

        flash(f'IMC: {imc} - Classificação: {classificacao}', 'sucess')

        # Gravar na session
        novo_calculo = {
            'nome' : nome,
            'peso' : peso,
            'altura' : altura,
            'imc' : imc,
            'classificacao' : classificacao
        }
        
        # Verifica se existe calculos na session, se não, cria ele vazio
        if 'calculos' not in session:
            session['calculos'] = []

        # adiciona o calculo na session
        session['calculos'].append(novo_calculo)

        # Avisa que a session mudou
        session.modified = true 

        return redirect(url_for('resultados'))

    return render_template('formulario.html')


if __name__ == '__main__':
    app.run(debug=True)
