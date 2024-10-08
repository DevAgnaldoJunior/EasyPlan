import streamlit as st
import pandas as pd
import json
import subprocess
import base64


# Função para salvar dados em um arquivo JSON
def save_to_json(data):
    with open('dados.json', 'w') as f:
        json.dump(data, f)

# Título da aplicação
st.title("Atualização de Datas e Anexar Planilhas")

# Widgets de data
data_inicio_input = st.date_input("Data de Início", value=pd.Timestamp('2024-08-25').date())
data_fim_input = st.date_input("Data de Fim", value=pd.Timestamp('2024-08-31').date())
data_inicio_antiga_input = st.date_input("Data de Início Antiga", value=pd.Timestamp('2024-08-18').date())
data_fim_antiga_input = st.date_input("Data de Fim Antiga", value=pd.Timestamp('2024-08-24').date())

# Uploader de arquivos
uploaded_files = {
    "tabela": st.file_uploader("Anexar Planilha de Acompanhamento Diário", type=['xlsx']),
    "tabela_projecao": st.file_uploader("Anexar Planilha de Projeção de Credenciais", type=['xlsx']),
    "credenciais": st.file_uploader("Anexar Tabela de Credenciais Utilizadas", type=['xlsx']),
    "report": st.file_uploader("Anexar Tabela de Report de Uso", type=['xlsx']),
}

# Botão de atualização
if st.button("Atualizar Datas e Carregar Planilhas"):
    # Armazenar dados de entrada
    config_data = {
        "data_inicio": str(data_inicio_input),
        "data_fim": str(data_fim_input),
        "data_inicio_antiga": str(data_inicio_antiga_input),
        "data_fim_antiga": str(data_fim_antiga_input),
        "files": {}
    }
    
    # Processar arquivos carregados
    for key, file in uploaded_files.items():
        if file is not None:
            try:
                # Lê o arquivo e o codifica em base64 para evitar problemas de leitura
                config_data["files"][key] = base64.b64encode(file.read()).decode('utf-8')
                st.success(f"{key.replace('_', ' ').title()} carregada com sucesso!")
            except Exception as e:
                st.error(f"Erro ao carregar {key.replace('_', ' ')}: {e}")

    # Salvar dados em JSON
    save_to_json(config_data)





if st.button("Executar Notebook"):
    try:
        jupyter_command = f"{sys.executable} -m jupyter nbconvert --to notebook --execute app.ipynb"
        result = subprocess.run(jupyter_command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            st.success("Notebook executado com sucesso!")
        else:
            st.error(f"Erro ao executar o notebook: {result.stderr}")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
