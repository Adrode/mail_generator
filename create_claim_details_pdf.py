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

reader_bg = PdfReader("./pdf_forms/claim_details.pdf")
page_bg = reader_bg.pages[0]

c = canvas.Canvas("test_claim_form_values1.pdf", pagesize=(595, 842))

draw_text(c, 297.50, 722.00, "nr autoryzacj/alias1 z dnia 14-10-2026:", size=12, align="center")
draw_text(c, 59, 662, "NAZWA SERWISU", size=12)
draw_text(c, 59, 642, "Ulicowa 99, 99-99 Ulicowo Górne", size=12)
draw_text(c, 358.20, 616.50, "10-10-2010")

draw_text(c, 158.76, 586, "DSR65420")
draw_text(c, 158.76, 569, "Opel Astra")
draw_text(c, 158.76, 552, "VINVINNICKI1230SDASDSD")
draw_text(c, 158.76, 535, "2005")
draw_text(c, 425.25, 586, "Klient")
draw_text(c, 425.25, 580, "Adrian COMPANY LTD. Adrian COMPANY LTD.", max_width=110, max_height=100, max_chars=30)
draw_text(c, 425.25, 535, "999888777")

draw_text(c, 158.76, 508, "2026-123543123123")
draw_text(c, 158.76, 491, "NR2026-SKA123124112312")
draw_text(c, 425.25, 508, "AC")
draw_text(c, 425.25, 501.5, "Powszechny Zakład Ubezpieczeń S.A.", max_width=110, max_height=100, max_chars=40)

draw_text(c, 158.76, 455, "Premium premium classic premium premium classic premium", max_width=110, max_height=100, max_chars=40)
draw_text(c, 158.76, 389, "Tak")
draw_text(c, 425.25, 444, "Tak")

draw_text(c, 70, 320, "uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzeniauszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia uszkodzenia", normal=True, max_width=220, max_height=100)
draw_text(c, 307, 320, "opis opis opis opis opis opis opis opisopis opis opis opis opis opis opis opis opis opis opis opis opis opis opisopis opis opis opis opis opis opis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opisopis opis opis opis opis opis opis", normal=True, max_width=220, max_height=100)

c.showPage()
c.save()

reader_txt = PdfReader("test_claim_form_values1.pdf")
page_txt = reader_txt.pages[0]

page_bg.merge_page(page_txt)

writer = PdfWriter()
writer.add_page(page_bg)

with open("final_claim_form1.pdf", "wb") as f:
  writer.write(f)

os.remove("test_claim_form_values1.pdf")