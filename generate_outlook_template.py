import os
import time
import win32com.client as win32
from pathlib import Path
from html_parser import parse_html
from generate_pdf_form import fill_out_pdf_form

def generate_mail(html):
  template_data = parse_html(html)
  fill_out_pdf_form(html)

  outlook = win32.Dispatch("Outlook.Application")

  mail = outlook.CreateItem(0)

  mail.Subject = template_data["message_title"]
  mail.HTMLBody = template_data["message_header"] + template_data["message_body"]
  mail.To = "somebody@example.com"

  def check_if_file_exists():
    my_file = Path("./out-filled-form.pdf")

    start_time = time.time()
    max_duration_time = 10

    while not my_file.exists():
      if time.time() - start_time > max_duration_time:
        raise TimeoutError("PDF file was not generated or found")
      time.sleep(1)
    
    return mail.Attachments.Add(str(my_file.resolve()))

  check_if_file_exists()

  mail.Display()

  os.remove("out-filled-form.pdf")