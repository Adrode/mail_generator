import time
import win32com.client as win32
from pathlib import Path
from html_scraper.html_scraper import parse_html
from html_scraper.html_scraper import parse_data_for_pdf_forms
from pdf_generator.create_pdf import (
  create_claim_details_pdf,
  create_compensation_authorization_form,
  create_documents_authorization_form
)

script_dir = Path(__file__).resolve().parent
temporary_filled_forms_dir = script_dir.parent / "temporary_filled_forms"

def generate_mail(html):
  data = parse_html(html)
  data_for_pdf_forms = parse_data_for_pdf_forms(html)
  method_of_claim_settlement = data_for_pdf_forms["method_of_claim_settlement"]
  case_number = data_for_pdf_forms["case_number"]

  create_claim_details_pdf(data_for_pdf_forms)
  claim_details_file_name = f"{case_number}_claim_details.pdf"
  if "ac" in method_of_claim_settlement.lower():
    create_compensation_authorization_form(data_for_pdf_forms)
    compensation_authorization_file_name = f"{case_number}_compensation_authorization.pdf"
  elif "oc" in method_of_claim_settlement.lower():
    create_documents_authorization_form(data_for_pdf_forms)
    documents_authorization_file_name = f"{case_number}_documents_authorization.pdf"

  outlook = win32.Dispatch("Outlook.Application")

  mail = outlook.CreateItem(0)

  mail.Subject = data["message_title"]
  mail.HTMLBody = data["message_header"] + data["message_additional_info"] + data["message_body"]

  def add_attachments():
    claim_details_attachment = Path(temporary_filled_forms_dir / claim_details_file_name)
    if compensation_authorization_file_name:
      second_attachment = Path(temporary_filled_forms_dir / compensation_authorization_file_name)
    elif documents_authorization_file_name:
      second_attachment = Path(temporary_filled_forms_dir / documents_authorization_file_name)

    start_time = time.time()
    max_duration_time = 10

    if "naprawa na koszt klienta" not in method_of_claim_settlement:
      while not claim_details_attachment.exists() and not second_attachment.exists():
        if time.time() - start_time > max_duration_time:
          raise TimeoutError("PDF files was not generated or found")
        time.sleep(1)
      
      mail.Attachments.Add(str(claim_details_attachment.resolve()))
      mail.Attachments.Add(str(second_attachment.resolve()))
    else:
      while not claim_details_attachment.exists():
        if time.time() - start_time > max_duration_time:
          raise TimeoutError("PDF files was not generated or found")
        time.sleep(1)
      
      mail.Attachments.Add(str(claim_details_attachment.resolve()))

  add_attachments()

  mail.Display()

  for file_path in temporary_filled_forms_dir.glob("*"):
    if file_path.is_file():
        file_path.unlink()