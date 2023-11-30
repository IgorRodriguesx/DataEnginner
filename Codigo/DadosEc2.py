# -*- coding: utf-8 -*-
#Carregando dados em nosso banco de dados em uma EC2

#importanto bibliotecas necessárias
import io
import psycopg2
import pandas as pd

#carregando datasets
## dataset cobranca de pacientes
cobranca_pacientes = pd.read_csv(r'Datasets\inpatientCharges.csv')
cobranca_pacientes[' Average Covered Charges '] = cobranca_pacientes[' Average Covered Charges '].str.replace('$','')
cobranca_pacientes[' Average Total Payments '] = cobranca_pacientes[' Average Total Payments '].str.replace('$','')
cobranca_pacientes['Average Medicare Payments'] = cobranca_pacientes['Average Medicare Payments'].str.replace('$','')

diagnosticos = pd.read_csv(r'Datasets\datasets_180_408_data.csv')
diagnosticos.drop(diagnosticos.columns[len(diagnosticos.columns)-1], axis=1, inplace=True)

def carregar_dados(conn, df, tabela, colunas):
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header = False, index = False)
    output.seek(0)
    try:
        cur.copy_from(output, tabela, null = "", columns = colunas)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        
conn = psycopg2.connect(host='localhost', port='5432', database='postgres', user='admin', password='')
        
carregar_dados(conn, cobranca_pacientes, 'cobranca_paciente', ('definicao', 
                                                            'identificacao',
                                                            'nome', 
                                                            'endereco',
                                                            'cidade',
                                                            'estado',
                                                            'codigo_postal',
                                                            'regiao',
                                                            'total_cobrancas',
                                                            'media_custos_cobertos',
                                                            'media_pagamento_total',
                                                            'media_gastos_cuidados'))
 
carregar_dados(conn, diagnosticos, 'dados_analises', ('id',
                                                    'diagnostico',
                                                    'media_raio',
                                                    'media_textura',
                                                    'media_perimetro',
                                                    'media_area',
                                                    'media_suavidade',
                                                    'media_compactacao',
                                                    'media_concavidade',
                                                    'media_concavidade_pontos',
                                                    'media_simetria',
                                                    'media_dimensao_fractal',
                                                    'se_raio',
                                                    'se_textura',
                                                    'se_perimetro',
                                                    'se_area',
                                                    'se_suavidade',
                                                    'se_compactacao',
                                                    'se_concavidade',
                                                    'se_concavidade_pontos',
                                                    'se_simetria',
                                                    'se_dimensao_fractal',
                                                    'pior_raio',
                                                    'pior_textura',
                                                    'pior_perimetro',
                                                    'pior_area',
                                                    'pior_suavidade',
                                                    'pior_compactacao',
                                                    'pior_concavidade',
                                                    'pior_concavidade_pontos',
                                                    'pior_simetria',
                                                    'pior_dimensao_fractal'))
