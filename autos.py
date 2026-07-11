import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =====================================================================
#  ⚙️ CÓDIGO DO SITE (VISUAL PREMIUM + ROTAS DIRETAS DE BUSCA)
# =====================================================================
class VisualSiteHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        produto = query_params.get('p', [''])
        
        html_botoes = ""
        texto_resultados = ""
        
        # Correção da lista: Extrai a busca sem os colchetes ['']
        if produto and produto[0]:
            prod_texto = produto[0].strip()
            
            # --- CONFIGURAÇÃO DOS AFILIADOS ---
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_SHOPEE = "18325271196"
            ID_AFILIADO_AMAZON = "nsoc02-20"
            ID_AFILIADO_olx = "tf"       
            ID_AFILIADO_ALIEXPRESS = "tf"

            # Formatação de strings limpas para as buscas
            termo_ml = urllib.parse.quote_plus(prod_texto.replace(" ", "-"))
            termo_shopee = urllib.parse.quote_plus(prod_texto.lower().replace(" ", "-"))
            termo_amazon = urllib.parse.quote_plus(prod_texto)
            termo_olx = urllib.parse.quote_plus(prod_texto)
            termo_aliexpress = urllib.parse.quote_plus(prod_texto)

            # --- LINKS DAS LOJAS ---
            link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
            link_shopee = f"https://shopee.com.br/list/{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
            link_amazon = f"https://www.amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"
            link_olx = f"https://olx.com.br{termo_olx}"
            link_aliexpress = f"https://pt.aliexpress.com/wholesale?SearchText={termo_aliexpress}&af={ID_AFILIADO_ALIEXPRESS}"

            texto_resultados = "<h2>StockNegócios - Buscador Automotivo Ativo!</h2>"
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🛒 Ver no Mercado Livre</a>
                <a href="{link_shopee}" target="_blank" class="btn btn-shopee">🛍️ Ver na Shopee</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a>
                <a href="{link_olx}" target="_blank" class="btn btn-olx">💙 Ver na olx</a>
                <a href="{link_aliexpress}" target="_blank" class="btn btn-aliexpress" style="background-color: #FF4747; color: white;">Ver no AliExpress</a>
            </div>
            """

        html_pagina = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "stocknegocio",
      "alternateName": "Buscador de Ofertas Integrado tf",
      "url": "https://onrender.com",
      "applicationCategory": "ShoppingApplication",
      "operatingSystem": "All",
      "browserRequirements": "Requires HTML5 support",
      "description": "Buscador inteligente e automatizado de ofertas em tempo real. Compara preços instantaneamente e encontra cupons validados no Mercado Livre, Shopee, Amazon, Magalu e AliExpress.",
      "offers": {{
        "@type": "Offer",
        "price": "0.00",
        "priceCurrency": "BRL"
      }},
      "featureList": "Comparador de preços automático, busca integrada multiloja, redirecionamento seguro com tracking tf, integração direta com robô do Telegram"
    }}
    </script>

            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>StockNegócio - Buscador Automotivo</title>
            <style>
                body {{
                    margin: 0; padding: 0; background-color: #121214; color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh;
                }}
                .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: auto; }}
                h1 {{ font-size: 26px; margin-bottom: 5px; font-weight: 800; }}
                .sub {{ color: #a8a8b3; font-size: 16px; margin-bottom: 40px; }}
                form {{ width: 100%; display: flex; flex-direction: column; gap: 15px; }}
                input[type="text"] {{
                    width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px;
                    background-color: #202024; color: #ffffff; font-size: 16px; outline: none; box-sizing: border-box;
                }}
                input[type="text"]:focus {{ border-color: #00b37e; }}
                button {{
                    width: 100%; padding: 16px; border: none; border-radius: 8px;
                    background-color: #00b37e; color: #ffffff; font-size: 16px; font-weight: bold; cursor: pointer;
                }}
                h2 {{ font-size: 16px; color: #a8a8b3; margin-top: 30px; }}
                h2 span {{ color: #00b37e; }}
                .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 20px; }}
                .btn {{
                    display: block; padding: 16px; text-decoration: none; color: white; font-weight: bold;
                    border-radius: 8px; text-align: center; font-size: 15px;
                }}
                .btn-ml {{ background-color: #fff159; color: #333333; }}
                .btn-shopee {{ background-color: #ee4d2d; }}
                .btn-amazon {{ background-color: #ff9900; color: #111111; }}
                .btn-magalu {{ background-color: #0086ff; color: white; }}
                .btn-netshoes {{ background-color: #532d85; color: white; }}
                
                footer {{ width: 100%; padding: 15px; text-align: center; font-size: 12px; color: #737380; background-color: #1a1a1e; box-sizing: border-box; }}
                footer a {{ color: #00b37e; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏎️ StockNegócios</h1>
                <div class="sub">Clique Aqui 👇</div>
                
                <form action="/" method="GET">
                    <input type="text" name="p" value="{produto[0] if produto and produto[0] else ''}" placeholder="O que você quer buscar hoje?" required>
                    <button type="submit">🔍 Buscar Ofertas</button>
                </form>
                
                {texto_resultados}
                {html_botoes}
            </div>
            
            <footer>
                texto_lgpd = "Aviso de Transparência e Privacidade:\\n\\nO StockNegócios é um buscador automotivo independente de utilidade pública. Não coletamos, não armazenamos e não comercializamos nenhum dado pessoal ou histórico de busca dos usuários. Os botões de consulta e lojas utilizam links de redirecionamento oficiais com tags de afiliados. Ao realizar uma compra ou consulta por meio deles, você apoia a manutenção gratuita deste robô."
            </footer>
        </body>
        </html>
        """
        self.wfile.write(html_pagina.encode('utf-8'))

def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), VisualSiteHandler)
    server.serve_forever()

# =====================================================================
#  🤖 CÓDIGO DO ROBÔ DO TELEGRAM (FORMATO SEGURO E CORRIGIDO)
# =====================================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()

    # --- CONFIGURAÇÃO DOS AFILIADOS NO BOT ---
    ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
    ID_AFILIADO_SHOPEE = "18325271196"
    ID_AFILIADO_AMAZON = "nsoc02-20"
    ID_AFILIADO_olx = "tf"       
    ID_AFILIADO_ALIEXPRESS = "tf"         

    # Formatação usando quote_plus (Corrigido: adicionado termo_netshoes)
    termo_ml = urllib.parse.quote_plus(produto.replace(" ", "-"))
    termo_shopee = urllib.parse.quote_plus(produto.lower().replace(" ", "-"))
    termo_amazon = urllib.parse.quote_plus(produto)
    termo_olx = urllib.parse.quote_plus(produto)
    termo_aliexpress = urllib.parse.quote_plus(produto)

    # Links parametrizados corrigidos com as rotas exatas de busca (/list/, /s?k=, /busca/)
    link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_shopee = f"https://shopee.com.br/list/{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
    link_amazon = f"https://www.amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"
    link_olx = f"https://olx.com.br{termo_olx}"
    link_aliexpress = f"https://pt.aliexpress.com/wholesale?SearchText={termo_aliexpress}&af={ID_AFILIADO_ALIEXPRESS}"


    botoes_links = [
        [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
        [InlineKeyboardButton("🛍️ Ver na Shopee", url=link_shopee)],
        [InlineKeyboardButton("📦 Ver na Amazon", url=link_amazon)],
        [InlineKeyboardButton("💙 Ver na olx", url=link_olx)],
        [InlineKeyboardButton("🇨🇳 Ver no AliExpress", url=link_aliexpress)],
        [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
    ]

    structure_links = InlineKeyboardMarkup(botoes_links)

    await update.message.reply_text(
        f"Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
        reply_markup=structure_links,
        parse_mode="Markdown"
    )

async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Pode enviar o nome do novo produto que deseja buscar!")

if __name__ == '__main__':
    # ADICIONE APENAS ESTA LINHA ABAIXO (Ela liga o site junto com o Telegram):
    threading.Thread(target=ligar_site_producao, daemon=True).start()

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^buscar$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    application.run_polling()
