import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_records():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM tabela_dados LIMIT 100").fetchall()
    conn.close()
    return records

def insert_record(data):
    conn = get_db_connection()
    query = '''INSERT INTO tabela_dados (data_base, uf, tcb, sr, cliente, ocupacao, cnae_secao, cnae_subclasse, porte, modalidade, origem, indexador, numero_de_operacoes, a_vencer_ate_90_dias, a_vencer_de_91_ate_360_dias, a_vencer_de_361_ate_1080_dias, a_vencer_de_1081_ate_1800_dias, a_vencer_de_1801_ate_5400_dias, a_vencer_acima_de_5400_dias, total_a_vencer, vencido_acima_de_15_dias, carteira_ativa, carteira_inadimplida_arrastada, ativo_problematico) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    conn.execute(query, tuple(data.values()))
    conn.commit()
    conn.close()

def update_record(record_id, data):
    data = {key: value for key, value in data.items() if value}
    set_clause = ", ".join([f"{key} = ?" for key in data.keys()])

    query = f"UPDATE tabela_dados SET {set_clause} WHERE id = ?"
    values = list(data.values()) + [record_id]

    conn = get_db_connection()
    conn.execute(query, values)
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tabela_dados WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
