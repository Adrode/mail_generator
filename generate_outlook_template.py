import win32com.client as win32

outlook = win32.Dispatch("Outlook.Application")

mail = outlook.CreateItem(0)

mail.Subject = "Tytuł"
mail.HTMLBody = "<b>Treść</b>"
mail.To = "somebody@example.com"
# mail.Attachments.Add(r"path")

mail.Display()