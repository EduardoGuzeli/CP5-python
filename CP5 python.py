# Eduardo Guzeli Nogueira RM: 571143
# Gabriel Kenzo RM: 569780
import json
from datetime import datetime
usuarios = []
feedbacks = []
categorias = ("Ruim", "Regular", "Bom", "Excelente")

def cadastrar_usuario() -> None:
   """Cadastra um novo usuário."""
   nome = input("Nome: ").strip()
   while not nome:
       print("Nome inválido.")
       nome = input("Nome: ").strip()
   while True:
       try:
           idade = int(input("Idade: "))
           if idade > 0:
               break
           print("Idade inválida.")
       except ValueError:
           print("Digite um número.")
   usuarios.append({
       "id": len(usuarios) + 1,
       "nome": nome,
       "idade": idade,
       "profissao": input("Profissão: "),
       "tipo_usuario": input("Tipo de usuário: ")
   })
   print("Usuário cadastrado!")

def listar_usuarios() -> None:
   """Mostra os usuários cadastrados."""
   if not usuarios:
       print("Nenhum usuário cadastrado.")
       return
   for u in usuarios:
       print(f"{u['id']} - {u['nome']} | {u['idade']} anos | "
             f"{u['profissao']} | {u['tipo_usuario']}")

def receber_feedback() -> None:
   """Cadastra um feedback."""
   if not usuarios:
       print("Cadastre um usuário primeiro.")
       return
   listar_usuarios()
   while True:
       try:
           id_usuario = int(input("ID do usuário: "))
           usuario = next((u for u in usuarios if u["id"] == id_usuario), None)
           if usuario:
               break
           print("Usuário não encontrado.")
       except ValueError:
           print("ID inválido.")
   produto = input("Produto: ")
   while True:
       data = input("Data (DD/MM/AAAA): ")
       try:
           datetime.strptime(data, "%d/%m/%Y")
           break
       except ValueError:
           print("Data inválida.")
   while True:
       try:
           nota = float(input("Nota de 0 a 10: "))
           if 0 <= nota <= 10:
               break
           print("Nota deve estar entre 0 e 10.")
       except ValueError:
           print("Digite um número.")
   feedbacks.append({
       "id_usuario": id_usuario,
       "nome_usuario": usuario["nome"],
       "produto": produto,
       "data": data,
       "nota": nota,
       "texto": input("Feedback: ")
   })
   print("Feedback registrado!")

def calcular_media() -> float:
   """Calcula a média das notas."""
   return sum(f["nota"] for f in feedbacks) / len(feedbacks) if feedbacks else 0

def classificar(nota: float) -> str:
   """Define a categoria da nota."""
   if nota < 5:
       return categorias[0]
   if nota < 7:
       return categorias[1]
   if nota < 9:
       return categorias[2]
   return categorias[3]

def gerar_relatorio() -> None:
   """Mostra um resumo dos feedbacks."""
   if not feedbacks:
       print("Nenhum feedback cadastrado.")
       return
   contagem = {c: 0 for c in categorias}
   for f in feedbacks:
       contagem[classificar(f["nota"])] += 1
   matriz = [
       ["Categoria", "Quantidade"],
       ["Ruim", contagem["Ruim"]],
       ["Regular", contagem["Regular"]],
       ["Bom", contagem["Bom"]],
       ["Excelente", contagem["Excelente"]]
   ]
   print("\n===== RELATÓRIO =====")
   print("Usuários:", len(usuarios))
   print("Feedbacks:", len(feedbacks))
   print(f"Média: {calcular_media():.2f}")
   for linha in matriz:
       print(linha)

def feedbacks_produto() -> None:
   """Mostra os feedbacks de um produto."""
   produto = input("Produto: ").lower()
   encontrados = [f for f in feedbacks if f["produto"].lower() == produto]
   if not encontrados:
       print("Produto não encontrado.")
       return
   for f in encontrados:
       print(f"\nUsuário: {f['nome_usuario']}\nNota: {f['nota']}"
             f"\nData: {f['data']}\nFeedback: {f['texto']}")

def analise_avancada() -> None:
   """Mostra algumas informações extras."""
   if not feedbacks:
       print("Nenhum feedback cadastrado.")
       return
   produtos = {}
   for f in feedbacks:
       produtos.setdefault(f["produto"], []).append(f["nota"])
   for produto, notas in produtos.items():
       media = sum(notas) / len(notas)
       if media < 6:
           msg = "Precisa de melhorias."
       elif media >= 8:
           msg = "Boa avaliação."
       else:
           msg = "Avaliação regular."
       print(f"{produto}: {media:.2f} - {msg}")
   usuarios_feedback = {}
   for f in feedbacks:
       nome = f["nome_usuario"]
       usuarios_feedback[nome] = usuarios_feedback.get(nome, 0) + 1
   for nome, qtd in usuarios_feedback.items():
       if qtd > 5:
           print(f"{nome}: perfil engajado ({qtd} feedbacks).")

def salvar_json() -> None:
   """Salva os dados em JSON."""
   try:
       with open("dados_feedsmart.json", "w", encoding="utf-8") as arq:
           json.dump({"usuarios": usuarios, "feedbacks": feedbacks},
                     arq, indent=4, ensure_ascii=False)
       print("JSON salvo!")
   except OSError as erro:
       print("Erro:", erro)

def carregar_json() -> None:
   """Carrega os dados do JSON."""
   try:
       with open("dados_feedsmart.json", encoding="utf-8") as arq:
           dados = json.load(arq)
       usuarios.clear()
       feedbacks.clear()
       usuarios.extend(dados.get("usuarios", []))
       feedbacks.extend(dados.get("feedbacks", []))
       print("JSON carregado!")
   except FileNotFoundError:
       print("Arquivo JSON não encontrado.")
   except json.JSONDecodeError:
       print("JSON inválido.")

def salvar_txt() -> None:
   """Salva os dados em TXT."""
   try:
       with open("dados_feedsmart.txt", "w", encoding="utf-8") as arq:
           arq.write("USUARIOS\n")
           for u in usuarios:
               arq.write(f"{u['id']}|{u['nome']}|{u['idade']}|"
                         f"{u['profissao']}|{u['tipo_usuario']}\n")
           arq.write("FEEDBACKS\n")
           for f in feedbacks:
               arq.write(f"{f['id_usuario']}|{f['nome_usuario']}|"
                         f"{f['produto']}|{f['data']}|{f['nota']}|{f['texto']}\n")
       print("TXT salvo!")
   except OSError as erro:
       print("Erro:", erro)

def carregar_txt() -> None:
   """Carrega os dados do TXT."""
   try:
       with open("dados_feedsmart.txt", encoding="utf-8") as arq:
           linhas = [l.strip() for l in arq if l.strip()]
       usuarios.clear()
       feedbacks.clear()
       modo = ""
       for linha in linhas:
           if linha in ("USUARIOS", "FEEDBACKS"):
               modo = linha.lower()
               continue
           p = linha.split("|")
           if modo == "usuarios":
               usuarios.append({
                   "id": int(p[0]), "nome": p[1], "idade": int(p[2]),
                   "profissao": p[3], "tipo_usuario": p[4]
               })
           else:
               feedbacks.append({
                   "id_usuario": int(p[0]), "nome_usuario": p[1],
                   "produto": p[2], "data": p[3],
                   "nota": float(p[4]), "texto": p[5]
               })
       print("TXT carregado!")
   except FileNotFoundError:
       print("Arquivo TXT não encontrado.")
   except (ValueError, IndexError):
       print("TXT inválido.")

def menu() -> None:
   """Mostra o menu do sistema."""
   while True:
       print("""
===== FEEDSMART =====
1 - Cadastrar usuário
2 - Listar usuários
3 - Registrar feedback
4 - Gerar relatório
5 - Feedbacks por produto
6 - Análise avançada
7 - Salvar JSON
8 - Salvar TXT
9 - Carregar JSON
10 - Carregar TXT
0 - Sair
""")
       opcao = input("Escolha: ")
       match opcao:
           case "1":
               cadastrar_usuario()
           case "2":
               listar_usuarios()
           case "3":
               receber_feedback()
           case "4":
               gerar_relatorio()
           case "5":
               feedbacks_produto()
           case "6":
               analise_avancada()
           case "7":
               salvar_json()
           case "8":
               salvar_txt()
           case "9":
               carregar_json()
           case "10":
               carregar_txt()
           case "0":
               print("Obrigado por usar o FeedSmart!")
               break
           case _:
               print("Opção inválida.")

menu()