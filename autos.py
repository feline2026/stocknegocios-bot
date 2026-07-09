import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
ID_AFILIADO_AMAZON = "nsoc02-20"
ID_AFILIADO_MAGALU = "tf"
TOKEN = os.environ.get("TELEGRAM_TOKEN")

class VisualSiteHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200); self.send_header('Content-type', 'text/html; charset=utf-8'); self.end_headers()
    def do_GET(self):
        self.send_response(200); self.send_header('Content-type', 'text/html; charset=utf-8'); self.end_headers()
        prod_texto = ""; html_botoes = ""; texto_resultados = "<h2>StockNegócio - Buscador Automotivo Ativo!</h2>"
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        produto = query_params.get('p', [''])
        if produto and produto[0]:
            prod_texto = produto[0].strip()
            t_olx = urllib.parse.quote_plus(prod_texto)
            t_wm = urllib.parse.quote_plus(prod_texto.lower().replace(" ", "-"))
            t_ml = urllib.parse.quote_plus(prod_texto)
            t_az = urllib.parse.quote_plus(prod_texto)
            
            l_olx = f"https://olx.com.br{t_olx}"
            l_wm = f"https://webmotors.com.br{t_wm}"
            l_pl = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
            l_ml = f"https://mercadolivre.com.br{t_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
            l_az = f"https://amazon.com.br{t_az}&tag={ID_AFILIADO_AMAZON}"
            
            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2>"
            html_botoes = f'<div class="box-botoes"><a href="{l_olx}" target="_blank" class="btn" style="background-color: #6E0AD6; color: white;">🚘 Ver na OLX</a><a href="{l_wm}" target="_blank" class="btn" style="background-color: #E31C23; color: white;">🚙 Ver na Webmotors</a><a href="{l_pl}" target="_blank" class="btn" style="background-color: #00A859; color: white;">🚨 Consultar Placa (10% OFF)</a><a href="{l_ml}" target="_blank" class="btn btn-ml">🔧 Ver no Mercado Livre</a><a href="{l_az}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a></div>'
        html_pagina = f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>StockNegócio</title><style>body {{ margin: 0; padding: 0; background-color: #121212; color: #ffffff; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh; }} .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: 0 auto; }} h1 {{ font-size: 26px; }} .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 24px; }} .btn {{ display: block; width: 100%; padding: 16px; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; box-sizing: border-box; transition: transform 0.2s; }} .btn:hover {{ transform: scale(1.02); }} .btn-ml {{ background-color: #FFF159; color: #333333; }} .btn-amazon {{ background-color: #FF9900; color: #111111; }} .telegram {{ background-color: #00b37e; color: white; margin-top: 20px; }} input[type="text"] {{ width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px; background-color: #202024; color: #ffffff; font-size: 16px; box-sizing: border-box; }} button {{ width: 100%; padding: 16px; border: none; border-radius: 8px; background-color: #00b37e; color: white; font-size: 16px; font-weight: bold; margin-top: 10px; }} footer {{ width: 100%; padding: 15px; text-align: center; font-size: 12px; color: #737380; background-color: #1a1a1e; box-sizing: border-box; }} footer a {{ color: #00b37e; text-decoration: none; font-weight: bold; }}</style></head><body><div class="container"><h1>🏎️ StockNegócio</h1><div>{texto_resultados}</div><form action="/" method="GET"><input type="text" name="p" value="{prod_texto}" placeholder="O que deseja buscar?"><button type="submit">Buscar Ofertas</button></form>{html_botoes}<a href="https://t.me" target="_blank" class="btn telegram">💬 Abrir no Telegram</a></div><footer>Buscador gratuito e independente de utilidade pública. <a href="#" onclick="alert('Aviso de Transparência:\\n\\nNão coletamos dados pessoais.')">Aviso de Transparência</a></footer></body></html>"""
        self.wfile.write(html_pagina.encode('utf-8'))

def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', porta), VisualSiteHandler).serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Olá! Envie o nome de um veículo ou produto para buscar:")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()
    t_site = urllib.parse.quote_plus(produto)
    t_olx = urllib.parse.quote_plus(produto)
    t_wm = urllib.parse.quote_plus(produto.lower().replace(" ", "-"))
    t_ml = urllib.parse.quote_plus(produto)
    t_az = urllib.parse.quote_plus(produto)
    
    url_site = f"https://onrender.com{t_site}"
    url_olx = f"https://olx.com.br{t_olx}"
    url_wm = f"https://webmotors.com.br{t_wm}"
    url_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
    url_ml = f"https://mercadolivre.com.br{t_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    url_amazon = f"https://amazon.com.br{t_az}&tag={ID_AFILIADO_AMAZON}"
    
    botoes = [
        [InlineKeyboardButton("🌐 Ver no Mercado Livre", url=url_ml)],
        [InlineKeyboardButton("🌐 Ver na Amazon", url=url_amazon)],
        [InlineKeyboardButton("🚘 Ver na OLX", url=url_olx)],
        [InlineKeyboardButton("🚙 Ver na Webmotors", url=url_wm)],
        [InlineKeyboardButton("🚨 Consultar Placa (10% OFF)", url=url_placa)],
        [InlineKeyboardButton("🌐 Ver no Site Visual tf", url=url_site)],
        [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
    ]
    await update.message.reply_text(f"Resultados para: *{produto}*\nClique abaixo:", reply_markup=InlineKeyboardMarkup(botoes), parse_mode="Markdown")

async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer(); context.user_data.clear(); await update.callback_query.message.reply_text("Pode enviar a nova busca!")

if __name__ == '__main__':
    threading.Thread(target=ligar_site_producao, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^buscar$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    app.run_polling()
