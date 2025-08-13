import uuid
import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index ():
    return render_template("index.html")

UPLOAD = 'static/assets'
app.config['UPLOAD'] = UPLOAD

@app.route('/cadastro_plataformas', methods=['GET', 'POST'])
def cadastro_plataformas():
    if request.method == 'POST':
        nome = request.form['nome']
        fabricante = request.form['fabricante']
        
        imagem = request.files['imagem']
        if imagem:
            extensao = imagem.filename.split('.')[-1]
            nome_imagem = f"{nome.strip().lower().replace(" ", "_")}.{extensao}" # f é para concatenar, ou seja, juntar// lower deixa o texto em minusculo// replace troca o espaço vazio por _// o ponto separa as informações da extesão como png
            caminho_imagem = os.path.join(app.config ['UPLOAD'], nome_imagem)
            imagem.save(caminho_imagem)
            
            
        cod_plataforma = str (uuid.uuid4())

        caminho_arquivo = 'models/plataforma.txt'

        with open(caminho_arquivo, 'a') as arquivo:
            arquivo.write(f"{nome};{fabricante};{cod_plataforma}\n")

        return redirect ("cadastro_plataformas")

    return render_template ("cadastro_plataformas.html")

#consulta de dados da página consulta_platafaorma.html
 
@app.route('/consulta_plataforma')
def consulta_plataforma():
    plataformas = []
    linha_controle = 0
    caminho_plataformas = 'models/plataforma.txt'
    
    with open(caminho_plataformas, 'r') as arquivo:
        for linha in arquivo:
            dados = linha
            #comando strip() elimina espaço em branco
            #comando split() divide informação baseado no caractere
            dados = linha.strip().split(';')
            plataformas.append({ 
                'linha': linha_controle,
                'cod_plataforma': dados[0],
                'nome': dados[1],
                'fabricante': dados[2]
            })
            linha_controle += 1 #incremento da var linha

        return render_template('consulta_plataforma.html', dados_lista=plataformas)
    
# Exclusão de dados do arquivo plataforma.txt
@app.route('/excluir_plataforma', methods=['GET', 'POST'])
def excluir_plataforma():
    linha_para_excluir = int (request.args.get('linha'))
    caminho_plataformas = 'models/plataforma.txt'

    with open(caminho_plataformas, 'r') as arquivo:
        linhas = arquivo.readlines() #cria a variável linhas que recebe todo o contexto

    del linhas[linha_para_excluir]

    with open(caminho_plataformas, 'w') as arquivo: # w reescreve
        arquivo.writelines(linhas)

    return redirect('/consulta_plataforma')

app.run(host='127.0.0.1', port=80, debug=True) #debug atualiza em tempo real