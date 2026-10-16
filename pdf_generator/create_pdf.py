import os
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

script_dir = Path(__file__).resolve().parent
pdf_forms_dir = script_dir / "pdf_forms"
temporary_filled_forms_dir = script_dir.parent / "temporary_filled_forms"

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

def create_claim_details_pdf(data):
  reader_bg = PdfReader(pdf_forms_dir / "claim_details.pdf")
  page_bg = reader_bg.pages[0]

  c = canvas.Canvas("claim_form_temporary_file.pdf", pagesize=(595, 842))

  draw_text(c, 297.50, 722.00, f"nr {data["case_number"]}/{data["alias"]} z dnia {data["date_of_incident"]}:", size=12, align="center")
  draw_text(c, 59, 662, data["car_service_name"], size=12)
  draw_text(c, 59, 642, data["car_service_address"], size=12)
  draw_text(c, 358.20, 616.50, data["date_of_incident"])

  draw_text(c, 158.76, 586, data["registration_number"])
  draw_text(c, 158.76, 569, data["make_and_model"])
  draw_text(c, 158.76, 552, data["vin"])
  draw_text(c, 158.76, 535, data["model_year"])
  draw_text(c, 425.25, 586, data["owner"])
  draw_text(c, 425.25, 580, data["client_name"], max_width=110, max_height=100, max_chars=30)
  draw_text(c, 425.25, 535, data["phone_number"])

  draw_text(c, 158.76, 508, data["insurance_policy_number"])
  draw_text(c, 158.76, 491, data["claim_number"])
  draw_text(c, 425.25, 508, data["method_of_claim_settlement"])
  draw_text(c, 425.25, 501.5, data["insurer_name"], max_width=110, max_height=100, max_chars=40)

  draw_text(c, 158.76, 455, data["assistance_package"], max_width=110, max_height=100, max_chars=40)
  draw_text(c, 158.76, 389, data["replacement_vehicle_guarantee"])
  draw_text(c, 425.25, 444, data["door_to_door_service"])

  draw_text(c, 70, 320, data["car_damage"], normal=True, max_width=220, max_height=100)
  draw_text(c, 307, 320, data["description_of_incident"], normal=True, max_width=220, max_height=100)

  c.showPage()
  c.save()

  reader_txt = PdfReader("claim_form_temporary_file.pdf")
  page_txt = reader_txt.pages[0]

  page_bg.merge_page(page_txt)

  writer = PdfWriter()
  writer.add_page(page_bg)

  with open(temporary_filled_forms_dir / f"{data["case_number"]}_claim_details.pdf", "wb") as f:
    writer.write(f)

  os.remove("claim_form_temporary_file.pdf")

def create_documents_authorization_form(data):
  reader_bg = PdfReader(pdf_forms_dir / "authorization_to_collect_documents.pdf")
  page_bg = reader_bg.pages[0]

  c = canvas.Canvas("doc_form_temporary_file.pdf", pagesize=(595, 842))

  draw_text(c, 59, 740, f"Wrocław, dnia {datetime.now().date().strftime("%d-%m-%Y")}", normal=True)
  draw_text(c, 536, 720, data["insurer_name"], size=13, align="right")
  # draw_text(c, 536, 700, "Al. JANA PAWŁA II 24", size=13, align="right")
  # draw_text(c, 536, 680, "00-133 WARSZAWA", size=13, align="right")

  draw_text(c, 157, 652.50, data["date_of_incident"], normal=True)
  draw_text(c, 157, 635, data["claim_number"], normal=True)
  draw_text(c, 157, 616.5, data["make_and_model"], normal=True)
  draw_text(c, 157, 598.8, data["registration_number"], normal=True)
  draw_text(c, 157, 580.5, data["contract_number"], normal=True)

  draw_text(c, 80, 425, data["car_service_name"], size=13)
  draw_text(c, 80, 407, data["car_service_address"], size=13)
  c.showPage()
  c.save()

  reader_txt = PdfReader("doc_form_temporary_file.pdf")
  page_txt = reader_txt.pages[0]

  page_bg.merge_page(page_txt)

  writer = PdfWriter()
  writer.add_page(page_bg)

  with open(temporary_filled_forms_dir / f"{data["case_number"]}_documents_authorization.pdf", "wb") as f:
    writer.write(f)

  os.remove("doc_form_temporary_file.pdf")

def create_compensation_authorization_form(data):
  reader_bg = PdfReader(pdf_forms_dir / "authorization_to_collect_compensation.pdf")
  page_bg = reader_bg.pages[0]

  c = canvas.Canvas("compensation_form_temporary_file.pdf", pagesize=(595, 842))

  draw_text(c, 59, 740, f"Wrocław, dnia {datetime.now().date().strftime("%d-%m-%Y")}", normal=True)
  draw_text(c, 536, 720, data["insurer_name"].upper(), size=13, align="right")
  # draw_text(c, 536, 700, "Al. JANA PAWŁA II 24", size=13, align="right")
  # draw_text(c, 536, 680, "00-133 WARSZAWA", size=13, align="right")

  draw_text(c, 157, 652.50, data["date_of_incident"], normal=True)
  draw_text(c, 157, 635, data["claim_number"], normal=True)
  draw_text(c, 157, 616.5, data["make_and_model"], normal=True)
  draw_text(c, 157, 598.8, data["registration_number"], normal=True)
  draw_text(c, 157, 580.5, data["contract_number"], normal=True)

  draw_text(c, 80, 450, data["car_service_name"], size=13)
  draw_text(c, 80, 432, data["car_service_address"], size=13)
  c.showPage()
  c.save()

  reader_txt = PdfReader("compensation_form_temporary_file.pdf")
  page_txt = reader_txt.pages[0]

  page_bg.merge_page(page_txt)

  writer = PdfWriter()
  writer.add_page(page_bg)

  with open(temporary_filled_forms_dir / f"{data["case_number"]}_compensation_authorization.pdf", "wb") as f:
    writer.write(f)

  os.remove("compensation_form_temporary_file.pdf")