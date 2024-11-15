import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from config import Config

plt.switch_backend('Agg')

def create_graphs():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM tabela_dados LIMIT 100", conn)
    conn.close()
    
    plt.figure(figsize=(14, 6))
    ax = plt.gca()
    df[['a_vencer_ate_90_dias', 'a_vencer_de_91_ate_360_dias', 
        'a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 
        'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']].plot(
        kind='bar', stacked=True, ax=ax
    )

    plt.title('Valores Totais a Vencer por Intervalo de Tempo')
    plt.xlabel('Índice')
    plt.ylabel('Total a Vencer (R$)')

    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('R$ {x:,.0f}'))
    stacked_bar_path = os.path.join(Config.STATIC_FOLDER, 'img/stacked_bar.png')

    plt.savefig(stacked_bar_path, bbox_inches='tight')
    plt.close()

    return stacked_bar_path
