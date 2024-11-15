from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['DATABASE'] = 'db/dados.db'
app.secret_key = os.urandom(24)

# Função para conectar no banco de dados
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Rota da página inicial com formulário
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)

        if file:
            # Salvando o arquivo na pasta uploads
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            try:
                # Processando o arquivo com pandas e inserindo os dados no banco
                df = pd.read_csv(file_path, sep=';', encoding='cp858')
                df['data_base'] = pd.to_datetime(df['data_base'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

                for column in ['a_vencer_ate_90_dias', 'a_vencer_de_91_ate_360_dias', 'a_vencer_de_361_ate_1080_dias',
                               'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']:
                    df[column] = df[column].str.replace(',', '.').astype(float)

                df['total_a_vencer'] = (df['a_vencer_ate_90_dias'] + df['a_vencer_de_91_ate_360_dias'] +
                                        df['a_vencer_de_361_ate_1080_dias'] + df['a_vencer_de_1081_ate_1800_dias'] +
                                        df['a_vencer_de_1801_ate_5400_dias'] + df['a_vencer_acima_de_5400_dias'])
                total_a_vencer_col = df.pop('total_a_vencer')
                df.insert(19, 'total_a_vencer', total_a_vencer_col)

                df.replace('-', None, inplace=True)
                conn = get_db_connection()
                
                # Inserindo cada linha no banco de dados
                for _, row in df.iterrows():
                    conn.execute(
                        '''INSERT INTO tabela_dados (data_base, uf, tcb, sr, cliente, ocupacao, 
                        cnae_secao, cnae_subclasse, porte, modalidade, origem, indexador, 
                        numero_de_operacoes, a_vencer_ate_90_dias, a_vencer_de_91_ate_360_dias, 
                        a_vencer_de_361_ate_1080_dias, a_vencer_de_1081_ate_1800_dias, 
                        a_vencer_de_1801_ate_5400_dias, a_vencer_acima_de_5400_dias, total_a_vencer, 
                        vencido_acima_de_15_dias, carteira_ativa, carteira_inadimplida_arrastada, 
                        ativo_problematico) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                        row
                    )
                conn.commit()
                conn.close()

                flash('Arquivo processado com sucesso!')
            except Exception as e:
                flash(f'Ocorreu um erro ao processar o arquivo: {e}')
            return redirect(url_for('index'))

    return render_template('index.html')

# Inicializando o banco de dados (primeira vez)
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS tabela_dados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_base DATE, uf TEXT, tcb TEXT, sr TEXT, cliente TEXT, ocupacao TEXT, 
                    cnae_secao TEXT, cnae_subclasse TEXT, porte TEXT, modalidade TEXT, 
                    origem TEXT, indexador TEXT, numero_de_operacoes INTEGER, 
                    a_vencer_ate_90_dias REAL, a_vencer_de_91_ate_360_dias REAL, 
                    a_vencer_de_361_ate_1080_dias REAL, a_vencer_de_1081_ate_1800_dias REAL, 
                    a_vencer_de_1801_ate_5400_dias REAL, a_vencer_acima_de_5400_dias REAL, 
                    total_a_vencer REAL, vencido_acima_de_15_dias REAL, carteira_ativa REAL, 
                    carteira_inadimplida_arrastada REAL, ativo_problematico REAL)''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Inicializando o banco de dados antes de iniciar o app
    if not os.path.exists('db/dados.db'):
        os.makedirs('db', exist_ok=True)
        init_db()

    app.run(debug=True)
