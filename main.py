import os
import tkinter as tk
from PIL import Image
import pytesseract

# Sequência da roda europeia (sentido horário)
roda = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Pega vizinhos (esquerda e direita na roda)
def get_vizinhos(numero):
    idx = roda.index(numero)
    viz_esq = roda[(idx - 1) % 37]  # Vizinho à esquerda
    viz_dir = roda[(idx + 1) % 37]  # Vizinho à direita
    return [viz_esq, viz_dir]

# Função pra capturar a tela e prever
def capturar():
    try:
        # Caminho ajustado para Android
        screenshot_path = "/sdcard/screenshot.png"
        os.system(f"screencap {screenshot_path}")
        img = Image.open(screenshot_path)
        texto = pytesseract.image_to_string(img)

        # Pega todos os números válidos do histórico
        todos_numeros = []
        for palavra in texto.split():
            if palavra.isdigit() and 0 <= int(palavra) <= 36:
                num = int(palavra)
                if num not in todos_numeros[:37]:  # Evita repetidos nos 37 primeiros
                    todos_numeros.append(num)

        # Seleciona os 37 primeiros números (os mais recentes)
        if len(todos_numeros) >= 37:
            numeros = todos_numeros[:37]
            qtd_numeros = 37
        else:
            numeros = todos_numeros
            qtd_numeros = len(numeros)

        # Atualiza a janela com a quantidade de números encontrados
        label_numero.config(text=f"Números: {qtd_numeros}")

        # Faz a previsão se houver números
        if qtd_numeros >= 1:
            # Calcula a média pra determinar a dúzia base
            media = sum(numeros) / len(numeros)
            media_duzia = 1 if media <= 12 else 2 if media <= 24 else 3

            # Conta a frequência de cada dúzia
            duzia1 = sum(1 for n in numeros if 1 <= n <= 12)  # 1ª Dúzia (1-12)
            duzia2 = sum(1 for n in numeros if 13 <= n <= 24)  # 2ª Dúzia (13-24)
            duzia3 = sum(1 for n in numeros if 25 <= n <= 36)  # 3ª Dúzia (25-36)

            # Adiciona os vizinhos da roda (esquerda e direita, com peso menor)
            for num in numeros:
                vizinhos = get_vizinhos(num)
                for viz in vizinhos:
                    if 1 <= viz <= 12:
                        duzia1 += 0.5
                    elif 13 <= viz <= 24:
                        duzia2 += 0.5
                    elif 25 <= viz <= 36:
                        duzia3 += 0.5

            # Determina a dúzia mais frequente
            freq_duzia = max([(duzia1, 1), (duzia2, 2), (duzia3, 3)])[1]

            # Faz o cruzamento: média tem peso maior, ajustado pela frequência
            previsao_num = media_duzia if media_duzia == freq_duzia or qtd_numeros < 37 else freq_duzia if abs(duzia1 - duzia2) > 5 or abs(duzia2 - duzia3) > 5 else media_duzia

            # Define a previsão final
            previsao = "1ª Dúzia (1-12)" if previsao_num == 1 else "2ª Dúzia (13-24)" if previsao_num == 2 else "3ª Dúzia (25-36)"
            label_previsao.config(text=f"Próxima: {previsao}")
        else:
            label_previsao.config(text="Nenhum número encontrado")
    except Exception as e:
        label_previsao.config(text=f"Erro: {str(e)}")

# Cria a janela flutuante
root = tk.Tk()
root.title("Previsão")
root.geometry("200x100")  # Tamanho compacto
root.configure(bg="yellow")  # Fundo amarelo
root.attributes("-topmost", True)  # Fica por cima de tudo

# Botão e labels pra interface
btn_capturar = tk.Button(root, text="Capturar", bg="yellow", fg="black", command=capturar)
btn_capturar.pack(pady=5)

label_numero = tk.Label(root, text="Números: 0", bg="yellow", fg="black")
label_numero.pack()

label_previsao = tk.Label(root, text="Aguardando captura", bg="yellow", fg="black")
label_previsao.pack()

# Inicia a janela
if __name__ == "__main__":
    root.mainloop()
