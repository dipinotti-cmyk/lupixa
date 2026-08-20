# Monta o cartao de previa (og:image) do portfolio, 1200x630.
#
# O link do portfolio e colado numa proposta da Workana e no WhatsApp. Sem
# og:image a previa sai sem imagem; com uma imagem generica sai pior ainda.
# Este cartao usa os prints reais dos cinco projetos que ja estao no topo da
# pagina, no mesmo preto do site.
#
#   python build-og.py
#
# Precisa de Pillow. Roda offline e o resultado (og-portfolio.jpg) e commitado.

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

L, A = 1200, 630
FUNDO = (10, 10, 10)
AMARELO = (250, 204, 21)
BRANCO = (245, 245, 245)

RAIZ = os.path.dirname(os.path.abspath(__file__))
FONTES = "C:/Windows/Fonts"
serif_bold = ImageFont.truetype(f"{FONTES}/georgiab.ttf", 52)
serif_bolditalic = ImageFont.truetype(f"{FONTES}/georgiaz.ttf", 52)
sans = ImageFont.truetype(f"{FONTES}/arial.ttf", 21)

cartao = Image.new("RGB", (L, A), FUNDO)

# Brilho do hero: duas manchas borradas, roxo e azul, no topo.
brilho = Image.new("RGB", (L, A), FUNDO)
d = ImageDraw.Draw(brilho)
d.ellipse([180, -260, 700, 260], fill=(46, 26, 74))
d.ellipse([560, -300, 1120, 220], fill=(20, 34, 72))
cartao = Image.blend(cartao, brilho.filter(ImageFilter.GaussianBlur(120)), 0.85)

d = ImageDraw.Draw(cartao)


def centrado(texto, fonte, y, cor):
    x0, y0, x1, y1 = d.textbbox((0, 0), texto, font=fonte)
    d.text(((L - (x1 - x0)) / 2 - x0, y), texto, font=fonte, fill=cor)


centrado("Você recebeu minha proposta.", serif_bold, 92, BRANCO)
centrado("Aqui está o que eu já entreguei.", serif_bolditalic, 158, AMARELO)

# Os cinco prints que abrem a pagina, na mesma ordem.
prints = [
    "home-gold-hero.webp",
    "home-loudrock-hero.webp",
    "home-leadflow-hero.webp",
    "home-m5-hero.webp",
    "home-setpoint-hero.webp",
]
larg, alt, gap = 196, 147, 18
total = len(prints) * larg + (len(prints) - 1) * gap
x = (L - total) // 2
topo = 300

for nome in prints:
    caminho = os.path.join(RAIZ, nome)
    with Image.open(caminho) as im:
        im = im.convert("RGB")
        # recorta pelo topo: o que identifica o projeto e o cabecalho do site
        proporcao = larg / im.width
        im = im.resize((larg, max(alt, round(im.height * proporcao))), Image.LANCZOS)
        im = im.crop((0, 0, larg, alt))
        cartao.paste(im, (x, topo))
    d.rectangle([x, topo, x + larg - 1, topo + alt - 1], outline=(255, 255, 255), width=1)
    x += larg + gap

rodape = "Top 1% Workana  ·  5,0 no Google  ·  18 projetos reais no ar em 2026"
centrado(rodape, sans, 505, (190, 190, 190))
centrado("lupixa.com", ImageFont.truetype(f"{FONTES}/arialbd.ttf", 19), 556, AMARELO)

destino = os.path.join(RAIZ, "og-portfolio.jpg")
cartao.save(destino, "JPEG", quality=88, optimize=True, progressive=True)
print("gerado:", destino, os.path.getsize(destino), "bytes")
