import pandas as pd
import matplotlib.pyplot as plt

def gerar_relatorio(instrucao):
    # Aqui você conectaria ao banco ou planilha para buscar dados
    # Simulando um resultado simples
    df = pd.DataFrame({
        'Dia': ['01/03', '02/03', '03/03'],
        'Visitas': [100, 120, 140]
    })

    fig, ax = plt.subplots()
    ax.plot(df['Dia'], df['Visitas'], marker='o')
    ax.set_title(f"Relatório: {instrucao}")
    ax.set_ylabel("Visitas")
    ax.set_xlabel("Data")
    return fig
