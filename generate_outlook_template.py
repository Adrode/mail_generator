import win32com.client as win32
from html_parser import parse_html

template_data = parse_html()

outlook = win32.Dispatch("Outlook.Application")

mail = outlook.CreateItem(0)

mail.Subject = template_data["message_title"]
mail.HTMLBody = template_data["message_header"] + template_data["message_body"]
mail.To = "somebody@example.com"
# mail.Attachments.Add(r"path")

mail.Display()