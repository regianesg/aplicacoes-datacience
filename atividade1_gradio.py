import os
from datetime import datetime

import gradio as gr
import pandas as pd

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo", "telefone"]


def garantir_colunas():
    """Se o CSV antigo não tiver a coluna 'telefone', adiciona (vazia)."""
    if os.path.exists(ARQUIVO_CSV):
        df = pd.read_csv(ARQUIVO_CSV, dtype=str)
        if list(df.columns) != COLUNAS:
            for col in COLUNAS:
                if col not in df.columns:
                    df[col] = ""
            df = df[COLUNAS]
            df.to_csv(ARQUIVO_CSV, index=False)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo, telefone):
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome,
        "idade": idade,
        "convenio": convenio,
        "prioridade": prioridade,
        "motivo": motivo,
        "telefone": telefone,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)

    garantir_colunas()

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    ultimos = pd.read_csv(ARQUIVO_CSV, dtype=str).tail(5)

    # Retorna: mensagem, tabela e valores "limpos" para cada campo do formulário
    return (
        "Paciente cadastrado com sucesso!",
        ultimos,
        "",     # nome
        None,   # idade
        None,   # convenio
        1,      # prioridade (valor inicial do slider)
        "",     # motivo
        "",     # telefone
    )


with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")
    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade")
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
    )
    prioridade = gr.Slider(1, 5, step=1, value=1, label="Prioridade do atendimento")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    telefone = gr.Textbox(
        label="Telefone",
        placeholder="(11) 99999-9999",
        max_lines=1,
    )

    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")

    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo, telefone],
        outputs=[saida_msg, tabela, nome, idade, convenio, prioridade, motivo, telefone],
    )

demo.launch()
