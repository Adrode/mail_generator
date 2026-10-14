import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path_regular = "C:/Windows/Fonts/times.ttf"
font_path_bold = "C:/Windows/Fonts/timesbd.ttf"

pdfmetrics.registerFont(TTFont("TimesNewRoman", font_path_regular))
pdfmetrics.registerFont(TTFont("TimesNewRoman-Bold", font_path_bold))

DEFAULT_FONT = "TimesNewRoman-Bold"
DEFAULT_NORMAL_FONT = "TimesNewRoman"
DEFAULT_SIZE = 11

def draw_text(
  c,
  x,
  y,
  text,
  size=DEFAULT_SIZE,
  normal=False,
  align="left",
  max_width=None,
  max_height=100,
  max_chars=None
):
  safe_text = str(text) if text is not None else ""
  font_name = DEFAULT_NORMAL_FONT if normal else DEFAULT_FONT

  if max_chars and len(safe_text) > max_chars:
    safe_text = safe_text[:max_chars] + "..."
  
  if max_width is not None:
    style = ParagraphStyle(
      name="DynamicStyle",
      fontName=font_name,
      fontSize=size
    )

    p = Paragraph(safe_text, style)
    p.wrapOn(c, max_width, max_height)
    p.drawOn(c, x, y - p.height)

  else:
    c.setFont(font_name, size)
    if align == "right":
      c.drawRightString(x, y, safe_text)
    elif align == "center":
      c.drawCentredString(x, y, safe_text)
    else:
      c.drawString(x, y, safe_text)

reader_bg = PdfReader("./pdf_forms/authorization_to_collect_compensation.pdf")
page_bg = reader_bg.pages[0]

c = canvas.Canvas("test_claim_form_values3.pdf", pagesize=(595, 842))

draw_text(c, 59, 740, "Wrocław, dnia 14-10-2026", normal=True)
draw_text(c, 536, 720, "POWSZECHNY ZAKŁAD UBEZPIECZEŃ S.A.", size=15, align="right")
draw_text(c, 536, 700, "Al. JANA PAWŁA II 24", size=15, align="right")
draw_text(c, 536, 680, "00-133 WARSZAWA", size=15, align="right")

draw_text(c, 157, 652.50, "10-10-2010", normal=True)
draw_text(c, 157, 635, "KAKIŚ NUMER SZKODY", normal=True)
draw_text(c, 157, 616.5, "Opel Astra", normal=True)
draw_text(c, 157, 598.8, "DSR65420", normal=True)
draw_text(c, 157, 580.5, "SMTH", normal=True)

draw_text(c, 80, 450, "NAZWA SERWISU", size=13)
draw_text(c, 80, 432, "Ulicowa 99, 99-99 Ulicowo Górne", size=13)
c.showPage()
c.save()

reader_txt = PdfReader("test_claim_form_values3.pdf")
page_txt = reader_txt.pages[0]

page_bg.merge_page(page_txt)

writer = PdfWriter()
writer.add_page(page_bg)

with open("final_claim_form3.pdf", "wb") as f:
  writer.write(f)

os.remove("test_claim_form_values3.pdf")