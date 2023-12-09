# -*- coding: utf-8 -*-
"""Monografia_JoãoVaz.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UZfUfaNcnUI9JxwPf1MfRRB88Y_hufmq

# MONOGRAFIA II
Tema: Detecção de discursos racistas no *Twitter*: Uma abordagem baseada em Aprendizado de Máquina e Processamento de Linguagem Natural.

Discente: João Vítor Vaz

Orientador: Jadson Gertrudes

##Pacotes##
"""


"""## Bibliotecas ##

"""

import nltk
import csv
import re
#import ftfy
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from IPython.display import display, HTML
import requests
from io import StringIO
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from IPython.display import display, HTML
from sklearn.model_selection import cross_val_score
import numpy as np

"""##Download StopWords em português##"""

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

"""##Tabela de dados"""

def exibir_tabela_personalizada(df):
    # Definir as opções de exibição para visualizar todas as colunas e linhas
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Personalizar a aparência da tabela
    table_style = """
    <style>
        th {
            font-weight: bold;
            text-align: center;
            background-color: #f2f2f2;
            padding: 8px;
        }
        td {
            text-align: left;
            padding: 8px;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
    """

    # Exibir a tabela com estilo personalizado
    display(HTML(table_style))
    display(df)

"""##Limpando arquivos e mantendo somente as colunas "text" e "racism" de cada base de dados##

"""

# arquivo
caminho_arquivo_saida = 'dadosComRacismo.csv'  # Atualize com o caminho para o seu arquivo CSV
df = pd.read_csv(caminho_arquivo_saida)

# Filtra as linhas com valor igual a 1 na coluna 'RACISM'
df_filtered = df[df['RACISM'] == 1]

# Mantém somente as colunas 'TEXT' e 'RACISM'
df_filtered = df_filtered[['TEXT', 'RACISM']]

df_filtered.to_csv(caminho_arquivo_saida, index=False)

print('Arquivo CSV "dadosComRacismo.csv" criado com sucesso!')

"""##Removendo os usuários, sequências de RT, símbolos, números, pontuação e links da planilha com todos os dados##

"""

url = 'https://docs.google.com/spreadsheets/d/1IfRgUY1vM4Xb7kRm9T4II-V8Y4D_OYWsms4v0fOtqhI/export?format=csv'

# Ler o arquivo CSV diretamente do link
response = requests.get(url)
data = StringIO(response.text)
df = pd.read_csv(data)

# Função para limpar os dados
def limpar_dados(texto):
    texto = str(texto)
   # texto = ftfy.fix_text(texto)  # Corrige erros de codificação de texto
    texto = texto.split("#")[0]
    texto = texto.split("https://")[0]
    texto = re.sub(r'k{2,}', '', texto) # Remover a sequência  de k's
    texto = re.sub(r'\d+', '', texto)  # Remove números
    texto = re.sub(r'@\w+\s?', '', str(texto))  # Remove o padrão "@algumusuario"
    texto = re.sub(r'\bRT\b', '', texto, flags=re.IGNORECASE)  # Remove a sequência "RT"
    texto = re.sub(r'\s?:\s?', ' ', texto)  # Remove o símbolo " : "
    texto = re.sub(r'https://\S+', '', texto)  # Remove trechos que começam com "https://" seguidos por qualquer sequência de caracteres não espaços em branco
    texto = re.sub(r'http://\S+', '', texto)  # Remove trechos que começam com "http://" seguidos por qualquer sequência de caracteres não espaços em branco
    texto = re.sub(r'[^\w\s]|_+', '', texto)  # Remove emojis
    texto = re.sub(r'"', '', texto)  # Remove aspas
    texto = re.sub(r'[^\w\s]', '', texto)  # Remove pontuação
    return texto

# Aplicar a limpeza na coluna 'TEXT'
df['TEXT'] = df['TEXT'].apply(limpar_dados)

def exibir_tabela_personalizada(df):
    pass

exibir_tabela_personalizada(df)

df.to_csv('arquivoSaida.csv', index=False)

"""##Transformando os tweets em minúsculo##

"""

df = pd.read_csv('arquivoSaida.csv')

# Função para pré-processamento de texto em minúsculo
def preprocess_lower(text):
    if isinstance(text, str):
        tokens = nltk.word_tokenize(text.lower(), language='portuguese')
        return ' '.join(tokens)
    else:
        return text

# Aplicar a função na coluna "TEXT"
df['TEXT'] = df['TEXT'].apply(preprocess_lower)

exibir_tabela_personalizada(df)

df.to_csv('arquivoSaida.csv', index=False)

"""##Remoção de StopWords##

"""

df = pd.read_csv('arquivoSaida.csv')

#exibir_tabela_personalizada(df)

stop_words = set(stopwords.words('portuguese'))

# Função para remover as stopwords
def remove_stopwords(text):
    if isinstance(text, str):
        filtered_text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        return filtered_text
    else:
        return text

# Aplicar a função na coluna 'TEXT'
df['TEXT_STOPWORD'] = df['TEXT'].apply(remove_stopwords)

exibir_tabela_personalizada(df)

df.to_csv('arquivoSaida.csv', index=False)

"""##Fazendo a Tokenização e criando uma coluna nova na tabela##"""

df = pd.read_csv('arquivoSaida.csv')

# Função para realizar a tokenização
def tokenize_text(text):
    if isinstance(text, str):
        tokens = word_tokenize(text, language='portuguese')
        return tokens
    else:
        return []

# Criar uma nova coluna 'TEXT_TOKENIZACAO' com as frases tokenizadas
df['TEXT_TOKENIZACAO'] = df['TEXT_STOPWORD'].apply(tokenize_text)

exibir_tabela_personalizada(df)

df.to_csv('arquivoSaida.csv', index=False)



from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# Todas as variáveis do código
dados = pd.read_csv('arquivoSaida.csv')
tweets = dados['TEXT_TOKENIZACAO'].tolist()
rótulos = dados['RACISM'].tolist()
df = pd.DataFrame({'TEXT_TOKENIZACAO': tweets, 'RACISM': rótulos})
majoritaria = df[df['RACISM'] == 0]
minoritaria = df[df['RACISM'] == 1]

valores_ngrama = [(1, 1), (2, 2), (3, 3), (4, 4)]
f_measures_under = []
media_acuracia_under = []
media_f1_under = []
media_acuracia_over = []
media_f1_over = []
estilo_tabela = """
<style>
    th {
        font-weight: bold;
        text-align: center;
        background-color: #f2f2f2;
    }
    td {
        text-align: center;
    }
    tr:nth-child(even) {
       text-align: center;
        background-color: #f9f9f9;
    }
</style>
"""

parametros_nb = {'alpha': [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]}
parametros_svm = {'C': [0.1, 1, 10, 100], 'gamma': [1, 0.1, 0.01, 0.001], 'kernel': ['rbf', 'poly', 'sigmoid']}
parametros_rl = {'C': [0.0001, 0.001, 0.01, 0.1, 1, 10.0, 100.0, 1000.0]}

def executar_experimento(ngram_range, modelo_escolhido, sampling_method):
    num_folds = 10
    vetorizador = TfidfVectorizer(ngram_range=ngram_range)
    X = vetorizador.fit_transform(tweets)

    # Aplicar SMOTE nos dados
    smote = SMOTE(random_state=42)
    X_smote, y_smote = smote.fit_resample(X, rótulos)

    # Dividir os dados em conjuntos de treinamento e teste
    X_treino, X_teste, y_treino, y_teste = train_test_split(X_smote, y_smote, test_size=0.3, random_state=42)

    if sampling_method == "undersampling":
        smote = SMOTE(random_state=42)
        X_treino_oversampled, y_treino_oversampled = smote.fit_resample(X_treino, y_treino)
        X_treino_sampled, y_treino_sampled = X_treino_oversampled, y_treino_oversampled
    elif sampling_method == "oversampling":
        minoritaria_oversampled = resample(minoritaria, replace=True, n_samples=len(majoritaria), random_state=42)
        dados_balanceados = pd.concat([majoritaria, minoritaria_oversampled])
        tweets_balanceados = dados_balanceados['TEXT_TOKENIZACAO'].tolist()
        rótulos_balanceados = dados_balanceados['RACISM'].tolist()
        X_balanceado = vetorizador.fit_transform(tweets_balanceados)
        X_treino_sampled, _, y_treino_sampled, _ = train_test_split(X_balanceado, rótulos_balanceados, test_size=0.3, random_state=42)
    else:
        raise ValueError("Método de amostragem desconhecido. Escolha 'undersampling' ou 'oversampling'.")

    if modelo_escolhido == "RL":
        modelo = LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)
        grid_search = GridSearchCV(modelo, parametros_rl, cv=num_folds, scoring='f1')
        grid_search.fit(X_treino_sampled, y_treino_sampled)
        modelo = LogisticRegression(C=grid_search.best_params_['C'], class_weight='balanced', random_state=42, max_iter=1000)
    elif modelo_escolhido == "NB":
        modelo = GaussianNB()
        X_treino_sampled = X_treino_sampled.toarray()
    elif modelo_escolhido == "SVM":
        modelo = SVC()
        grid_search = GridSearchCV(modelo, parametros_svm, cv=num_folds, scoring='f1')
        grid_search.fit(X_treino_sampled, y_treino_sampled)
        modelo = SVC(C=grid_search.best_params_['C'], gamma=grid_search.best_params_['gamma'], kernel=grid_search.best_params_['kernel'])
    else:
        raise ValueError("Modelo desconhecido. Escolha 'RL' para Regressão Logística, 'NB' para Naive Bayes ou 'SVM' para Support Vector Machine.")

    modelo.fit(X_treino_sampled, y_treino_sampled)
    from sklearn.metrics import mean_squared_error
    # Calcular o erro quadrático médio para os conjuntos de treinamento e teste
   
    # Fazer previsões no conjunto de treinamento
    if modelo_escolhido == "NB":
        y_pred_treino = modelo.predict(X_treino_sampled)
        y_pred_teste = modelo.predict(X_teste)
    else:
        y_pred_treino = modelo.predict(X_treino_sampled)
        y_pred_teste = modelo.predict(X_teste)

    # Calcular o erro quadrático médio para os conjuntos de treinamento e teste
    erro_treino = mean_squared_error(y_treino_sampled, y_pred_treino)
    erro_teste = mean_squared_error(y_teste, y_pred_teste)

    print(f'Erro de treinamento: {erro_treino}')
    print(f'Erro de teste: {erro_teste}')

    acuracia = accuracy_score(y_teste, y_pred_teste)
    f1 = f1_score(y_teste, y_pred_teste)

    cv_scores_accuracy = cross_val_score(modelo, X_treino_sampled, y_treino_sampled, cv=num_folds, scoring='accuracy')
    cv_scores_f1 = cross_val_score(modelo, X_treino_sampled, y_treino_sampled, cv=num_folds, scoring='f1')

    return cv_scores_accuracy, cv_scores_f1, acuracia, f1

modelo_escolhido = input("Digite 'RL', 'NB' ou 'SVM': ")
print()
print("Em execução...")

for ngram_range in valores_ngrama:
    cv_scores_accuracy_under, cv_scores_f1_under, acuracia_under, f1_under = executar_experimento(ngram_range, modelo_escolhido, "undersampling")
    cv_scores_accuracy_over, cv_scores_f1_over, acuracia_over, f1_over = executar_experimento(ngram_range, modelo_escolhido, "oversampling")

    mean_cv_accuracy_under = np.mean(cv_scores_accuracy_under)
    mean_cv_f1_under = np.mean(cv_scores_f1_under)
    mean_cv_accuracy_over = np.mean(cv_scores_accuracy_over)
    mean_cv_f1_over = np.mean(cv_scores_f1_over)

    media_acuracia_under.append(mean_cv_accuracy_under)
    media_f1_under.append(mean_cv_f1_under)
    media_acuracia_over.append(mean_cv_accuracy_over)
    media_f1_over.append(mean_cv_f1_over)

    print(f"N-grama: {ngram_range}")
    print(f"Média da Acurácia (Undersampled): {mean_cv_accuracy_under}")
    print(f"Média da Acurácia (Oversampled): {mean_cv_accuracy_over}")
    print(f"Média do F1 Score (Undersampled): {mean_cv_f1_under}")
    print(f"Média do F1 Score (Oversampled): {mean_cv_f1_over}")
    print()

print("Execução concluída!")