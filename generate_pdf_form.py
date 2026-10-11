from pypdf import PdfReader, PdfWriter
from html_parser import parse_data_for_pdf

def fill_out_pdf_form():
  data_for_pdf = parse_data_for_pdf()

  reader = PdfReader("claim_form.pdf")
  writer = PdfWriter()

  page = reader.pages[0]
  fields = reader.get_fields()

  writer.append(reader)

  writer.update_page_form_field_values(
    writer.pages[0],
    {
      "registration_number": data_for_pdf["registration_number"],
      "VIN": data_for_pdf["VIN"],
      "make_and_model": data_for_pdf["make_and_model"],
      "phone_number": data_for_pdf["phone_number"],
      "client_name": data_for_pdf["client_name"],
      "type_of_claim_settlement": data_for_pdf["method_of_claim_settlement"],
      "insurance_policy_number": data_for_pdf["insurance_policy_number"],
      "insurer_name": data_for_pdf["insurer_name"],
      "claim_number": data_for_pdf["claim_number"],
      "date_of_incident": data_for_pdf["date_of_incident"],
      "incident_description": data_for_pdf["description_of_incident"],
      "car_service_name": data_for_pdf["car_service_name"],
      "car_service_address": data_for_pdf["car_service_address"]
    },
    auto_regenerate=False,
  )

  writer.write("out-filled-form.pdf")