# 📄 README.md — Phishing Detector (Conceito C)

## 🛡️ Sobre o Projeto

Este projeto foi desenvolvido para a disciplina **Tecnologias Hackers**, seguindo a **Opção 3 – Ferramenta para Detecção de Phishing (Conceito C)**.

O objetivo é criar um sistema capaz de:

- Analisar URLs enviadas pelo usuário  
- Detectar características suspeitas comuns em páginas de phishing  
- Verificar se o domínio aparece em uma **blacklist real** baseada em dataset  
- Exibir os resultados em uma **interface web simples**

Este projeto **não usa API externa**, pois o OpenPhish Community Feed estava instável e retornando erros frequentes.  
Para garantir confiabilidade, foi adotada uma abordagem **offline** utilizando um dataset local contendo milhares de URLs maliciosas reais.

---

## 📂 Estrutura do Projeto

```
phishing-detector/
│
├── src/
│   ├── main.py                 # Aplicação Flask (backend)
│   ├── analyzer.py             # Lógica principal da análise
│   ├── blacklist_checker.py    # Verificação usando dataset local
│   ├── utils/
│   │   ├── url_parser.py       # Normalização e parsing da URL
│   │   └── indicators.py       # Heurísticas simples de detecção
│   └── requirements.txt        # Dependências do projeto
│
├── web/
│   ├── templates/
│   │   └── index.html          # Interface web
│   └── static/
│       ├── styles.css          # Estilos
│       └── script.js           # Lógica do frontend
│
├── data/
│   └── malicious_phish.csv     # Dataset local de URLs maliciosas
│
└── README.md
```

---

## 🧠 Lógica da Detecção

A análise é dividida em **duas camadas principais**:

### 1️⃣ Heurísticas Simples (detecção leve)

O módulo `utils/indicators.py` detecta sinais simples de phishing, como:

- Substituição de letras por números (`g00gle`, `paypa1`)  
- Uso excessivo de subdomínios  
- Caracteres especiais suspeitos (`@`, `%`, `=`, `&`)

Esses fatores podem classificar uma URL como:

- **safe**
- **suspicious**

---

### 2️⃣ Blacklist baseada em Dataset Local (detecção forte)

O sistema usa o dataset:

```
data/malicious_phish.csv
```

Este arquivo contém dezenas de milhares de URLs maliciosas rotuladas.  
O módulo `blacklist_checker.py`:

- Lê automaticamente o CSV  
- Identifica colunas (`url`, `type`)  
- Filtra apenas entradas marcadas como `"phishing"`  
- Normaliza URLs  
- Extrai o domínio (host)  
- Constrói uma lista negra local com milhares de hosts maliciosos  

Se um domínio analisado estiver nessa lista → **malicious**.

---

## 🖥️ Interface Web

Disponível em:

```
http://localhost:5000/
```

Permite:

- Inserir uma URL  
- Ver o status (verde/amarelo/vermelho)  
- Ver indicadores de suspeita  
- Ver razões da classificação  

---

## ▶️ Como Executar

### 1. Instalar dependências
```bash
pip install -r src/requirements.txt
```

### 2. Rodar o servidor
```bash
python src/main.py
```

### 3. Acessar no navegador
```
http://127.0.0.1:5000/
```

---

## 🧪 Como Testar

### ✔ URLs seguras:
```
https://google.com
https://github.com
```

### ✔ URLs suspeitas (heurísticas):
```
http://g00gle-login-check.net
http://login.verify.account.update.security.example.com
http://example.com/login?acc=1&token=%123
```

### ✔ URLs maliciosas vindas do dataset:
Abra `data/malicious_phish.csv`  
Encontre uma linha com:

- `type = phishing`  
- `url = http://dominio-malicioso.com/...`

Teste:

```
http://dominio-malicioso.com
```

Resultado esperado: **malicious**

---

## 📝 Logs do Terminal

Exemplo de saída:

```
[INFO] Colunas encontradas: ['url', 'type']
[INFO] Linhas lidas: 651191 — phishing: 94111
[INFO] Hosts únicos: 33585 — linhas ignoradas: 12
```

---

## 📌 Por que usar dataset local?

- API do OpenPhish estava instável  
- Dataset é **offline**, rápido e reprodutível  
- Evita falhas de rede  
- Garante consistência durante avaliação  
- Atende perfeitamente o conceito C  

---

## 📘 Entregáveis atendidos

- ✔ Heurísticas básicas  
- ✔ Blacklist real via dataset  
- ✔ Interface web  
- ✔ Logs claros  
- ✔ Código modular e limpo  
- ✔ README completo  

---

## 📂 Dataset de URLs maliciosas (malicious_phish.csv)

Para realizar a detecção baseada em blacklist, o projeto utiliza um dataset de URLs maliciosas (phishing).  
Como o arquivo original (`malicious_phish.csv`) é grande e não deve ser versionado no Git, ele é disponibilizado em formato compactado.

### 📥 Download do dataset

Baixe o arquivo ZIP com o dataset pelo link abaixo:

[⬇️ Baixar dataset (malicious_phish.zip)](<sandbox:/mnt/data/archive (1>).zip)

### 🗂️ Como usar o dataset no projeto

1. Faça o download do arquivo ZIP.
2. Extraia o arquivo `malicious_phish.csv`.
3. Coloque o arquivo extraído na seguinte pasta do projeto:

   ```text
   data/malicious_phish.csv


## 📬 Autor

Projeto desenvolvido por **Pedro Ribeiro** para **Tecnologias Hackers – Insper**.
