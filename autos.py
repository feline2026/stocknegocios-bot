import urllib.parse
import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
ID_AFILIADO_AMAZON = "nsoc02-20"
ID_AFILIADO_MAGALU = "tf"

# INSIRA SEU NOVO TOKEN E SUA CHAVE DO GEMINI AQUI:
TOKEN = "8645090278:AAHUJMZaDPdFYth8HwrV5uVlvZQwwU57bZE"
GEMINI_KEY = "AQ.Ab8RN6Li4Ur45FCEDf_XdUHeTxrXmvtUbxv8ynFnfKUXKq0ujA"

# FUNÇÃO REESTRUTURADA - REQUISIÇÃO DIRETA ESTÁVEL PARA O GEMINI IA
def obter_avaliacao_ia(nome_veiculo):
    api_key = GEMINI_KEY
    if not api_key or "SUA_CHAVE" in api_key:
        return "🤖 Avaliação Inteligente StockNegócios:\nInsira a chave GEMINI na linha 15 do arquivo do GitHub."
    
    # Rota estável HTTP que o site e o Telegram leem juntos sem conflito ou tela branca
    url = f"https://googleapis.com{api_key}"
    headers = {"Content-Type": "application/json"}
    prompt = f"Aja como um especialista em carros no Brasil. Diga de forma muito curta e resumida uma estimativa de preço médio de mercado atual para o veículo '{nome_veiculo}' e cite 2 pontos de atenção com emojis. Seja muito direto e breve."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        import httpx
        # Faz a chamada rápida ignorando travas locais do servidor Linux do Render
        response = httpx.post(url, json=payload, headers=headers, timeout=10.0, verify=False)
        if response.status_code == 200:
            dados = response.json()
            texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
            texto_limpo = texto_ia.replace("**", "").replace("*", "").replace("#", "")
            return texto_limpo
        return f"🤖 Avaliação: Veja as ofertas regionais nos botões abaixo. (HTTP {response.status_code})"
    except Exception:
        return "🤖 Avaliação Inteligente ativa! Confira as ofertas locais nos botões abaixo."

class VisualSiteHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200); self.send_header('Content-type', 'text/html; charset=utf-8'); self.end_headers()
        def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        prod_texto = ""
        html_botoes = ""
        texto_resultados = "<h2>StockNegócios - Buscador Automotivo Ativo!</h2>"
        
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        produto = query_params.get('p')
        
        if produto:
            prod_texto = produto[0].strip() if isinstance(produto, list) else produto.strip()
            termo_olx = urllib.parse.quote_plus(prod_texto)
            
            # Executa a chamada estável da IA para o site
            avaliacao_site = obter_avaliacao_ia(prod_texto)
            avaliacao_limpa = avaliacao_site.replace("**", "").replace("*", "").replace("#", "")
            avaliacao_html = avaliacao_limpa.replace("\n", "<br>")
            
            link_olx = f"https://olx.com.br{termo_olx}"
            link_ml = f"https://mercadolivre.com.br{termo_olx}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
            link_amazon = f"https://amazon.com.br{termo_olx}&i=automotive&tag={ID_AFILIADO_AMAZON}"
            link_aliexpress = f"https://tabelafipebrasil.com{termo_olx}"
            
            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2><div style='background: #1a1a1e; padding: 15px; border-radius: 8px; margin: 20px auto; text-align: left; font-size: 14px; line-height: 1.6; max-width: 100%; border-left: 4px solid #00b37e;'>{avaliacao_html}</div>"
            
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🔧 Ver no Mercado Livre</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Peças e Acessórios na Amazon</a>
                <a href="{link_olx}" target="_blank" class="btn" style="background-color: #6E0AD6; color: white;">🚘 Ver na OLX Autos (SP)</a>
                <a href="{link_aliexpress}" target="_blank" class="btn" style="background-color: #0056B3; color: white;">📊 Consultar Preço Tabela FIPE</a>
            </div>
            """
        
        texto_lgpd = "Aviso de Transparência e Privacidade:\\n\\nO StockNegócios é um buscador automotivo independente. Utiliza inteligência artificial para exibir as melhores ofertas com links de afiliados."

        html_pagina = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockNegócios - Buscador Automotivo</title>
    <style>
        body {{ margin: 0; padding: 0; background-color: #121212; color: #ffffff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh; }}
        .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: 0 auto; }}
        h1 {{ font-size: 26px; }}
        h2 {{ font-size: 16px; font-weight: normal; color: #a8a8b3; margin-bottom: 24px; }}
        h2 span {{ color: #00b37e; font-weight: bold; }}
        .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 24px; }}
        .btn {{ display: block; width: 100%; padding: 16px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; box-sizing: border-box; transition: transform 0.2s; }}
        .btn:hover {{ transform: scale(1.02); }}
        .btn-ml {{ background-color: #FFF159; color: #333333; }}
        .btn-amazon {{ background-color: #FF9900; color: #111111; }}
        input[type="text"] {{ width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px; background-color: #202024; color: #ffffff; font-size: 16px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 16px; border: none; border-radius: 8px; background-color: #00b37e; color: white; font-size: 16px; font-weight: bold; margin-top: 10px; cursor: pointer; }}
        footer {{ width: 100%; padding: 15px; text-align: center; font-size: 12px; color: #737380; background-color: #1a1a1e; box-sizing: border-box; }}
        footer a {{ color: #00b37e; text-decoration: none; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏎️ StockNegócios</h1>
        <div>{texto_resultados}</div>
        <form action="/" method="GET">
            <input type="text" name="p" value="{prod_texto}" placeholder="Qual carro deseja buscar?">
            <button type="submit">Buscar Ofertas</button>
        </form>
        {html_botoes}
    </div>
    <footer>Buscador automotivo gratuito e independente. <a onclick="alert('{texto_lgpd}')">Aviso de Transparência</a></footer>
</body>
</html>"""
        self.wfile.write(html_pagina.encode('utf-8'))

def ligar_site_producao():
    import threading
    porta = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', porta), VisualSiteHandler).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏎️ Olá! Envie o nome de um veículo para buscar ofertas e ver a avaliação com IA.")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()
    termo_olx = urllib.parse.quote_plus(produto)
    
    # Executa a chamada assíncrona da IA nativamente no fluxo do Telegram
    avaliacao_texto = await obter_avaliacao_ia_async(produto)
    
    link_site = f"https://onrender.com{termo_olx}"
    link_olx = f"https://olx.com.br{termo_olx}"
    link_ml = f"https://mercadolivre.com.br{termo_olx}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon = f"https://amazon.com.br{termo_olx}&i=automotive&tag={ID_AFILIADO_AMAZON}"
    link_aliexpress = f"https://tabelafipebrasil.com{termo_olx}"
    
    structure_links = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Ver no Mercado Livre", url=link_ml)],
        [InlineKeyboardButton("📦 Peças e Acessórios na Amazon", url=link_amazon)],
        [InlineKeyboardButton("🚘 Ver na OLX Autos (SP)", url=link_olx)],
        [InlineKeyboardButton("📊 Consultar Preço Tabela FIPE", url=link_aliexpress)],
        [InlineKeyboardButton("🔄 Buscar Outro Produto", callback_data="rebuscar_produto")]
    ])
    
    await update.message.reply_text(f"{avaliacao_texto}\n\n👇 *Confira as ofertas disponíveis:*", reply_markup=structure_links)

async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text(text="🏎️ Digite o nome do novo veículo que deseja buscar:")

if __name__ == '__main__':
    # Primeiro criamos a estrutura do Telegram
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    
    # Ligamos o site visual em segundo plano antes do Polling para não travar a porta
    import threading
    threading.Thread(target=ligar_site_producao, daemon=True).start()
    
    # E por fim damos o arranque final nas mensagens do celular
    application.run_polling()

