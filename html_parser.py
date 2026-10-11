from bs4 import BeautifulSoup

# with open("test.html", "r", encoding="UTF-8") as f:
#   test_html = f.read()

def find_text(element):
  return lambda text: text and element in text

def get_alias(soup):
  return (soup.find("table", id="topHeaderTable")
    .find("a")
    .find_previous_sibling("b")
    .get_text(strip=True)
  )

def get_vehicle_data(soup):
  vehicle_data = {
    "registration_number": (
      soup.find("td", string=find_text("Nr rejestracyjny"))
      .find_parent("tr")
      .find("a")
      .get_text(strip=True)
    ),
    "make_and_model": (
      soup.find("label", string=find_text("Pojazd:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "first_registration_date": (
      soup.find("label", string=find_text("Data pierwszej rejestracji:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "VIN": (
      soup.find("label", string=find_text("Nr nadwozia:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    )
  }

  return vehicle_data

def get_car_insurance_claim_data(soup):
  main_table = soup.find("table", class_="carInsuranceClaimBasicDataTable")

  car_insurance_claim_data = {
    "car_service_name": (
      main_table.find("a", id="serviceCompanyHref")
      .get_text(strip=True)
    ),
    "car_service_address": (
      main_table.find("td", string=find_text("Oddział:"))
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "case_number": (
      main_table.find("span", id="authorization_number_id")
      .get_text(strip=True)
    ),
    "insurer_name": (
      main_table.find("label", string=find_text("Nazwa ZU:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "claim_number": (
      main_table.find("label", string=find_text("Nr szkody:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "method_of_claim_settlement": (
      main_table.find("label", string=find_text("Sposób rozliczania:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "type_of_claim_damage": (
      main_table.find("label", string=find_text("Typ szkody:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "date_of_incident": (
      main_table.find("label", string=find_text("Data zdarzenia:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "description_of_incident": (
      main_table.find("div", string=find_text("Treść zlecenia:"))
      .find_next_sibling("div")
      .get_text(strip=True)
    ),
    "contact_person": (
      main_table.find("label", string=find_text("Osoba do kontaktu:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    )
  }
  
  return car_insurance_claim_data

def get_insurance_data(soup):
  if get_car_insurance_claim_data(soup):
    insurer_name = get_car_insurance_claim_data(soup)["insurer_name"]
  else:
    insurer_name = None

  insurance_data = {
    "insurance_source_1": (
      soup.find("label", string=find_text("Ubezpieczenie zakupione przez:"))
      .find_parent("td")
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    ),
    "insurance_source_2": (
      soup.find("th", string=find_text("Polisa"))
      .find_parent("table")
      .find("tbody")
      .find("tr")
      .select("td")[4]
      .get_text(strip=True)
    ),
    "insurer_name": insurer_name
  }

  return insurance_data

def get_car_damage_data(soup):
  return (
    soup.find("span", string=find_text("Uszkodzenia"))
    .find_parent("tr")
    .find_next_sibling("tr")
    .find_next_sibling("tr")
    .find("td")
    .get_text(strip=True)
  )

def get_contract_data(soup):
  main_table = soup.find("td", string=find_text("Data akt/zd:")).find_parent("table")
  
  contract_data = {
    "selected_claims_handling": (
      main_table.find("td", string=find_text("Zarządzanie likwidacją szkód:"))
      .find_next_sibling("td")
      .get_text(strip=True)
    ),
    "contract_status": (
      main_table.find("td", string=find_text("Stauts umowy:"))
      .find_next_sibling("td")
      .get_text(strip=True)
    ),
    "contract_end_date": (
      main_table.find("td", string=find_text("Data akt/zd:"))
      .find_next_sibling("td")
      .find("label")
      .get_text(strip=True)
    )
  }

  return contract_data

def get_client_data(soup):
  main_table = soup.find("a", string=find_text("Segment")).find_parent("table")

  client_data = {
    "user_name": (
      main_table.find("td", string=find_text("Nazwa"))
      .find_next_sibling("td")
      .find("a")
      .get_text(strip=True)
    ),
    "user_location": (
      main_table.find("label", string=find_text("Miasto:"))
      .find_parent("td")
      .find_next_sibling("td") 
      .find("label")
      .get_text(strip=True)
    ),
    "client_company_name": (
      main_table.find("td", string=find_text("Klient:"))
      .find_next_sibling("td")
      .find("a")
      .get_text(strip=True)
    ),
    "fleet_managers_contat_details": (
      main_table.find("td", string=find_text("Flotowiec:"))
      .find_next_sibling("td")
    )
  }

  return client_data

def parse_data_for_pdf(html):
  soup = BeautifulSoup(html, "html.parser")

  alias = get_alias(soup)
  vehicle_data = get_vehicle_data(soup)
  car_insurance_claim_data = get_car_insurance_claim_data(soup)
  insurance_data = get_insurance_data(soup)
  car_damage_data = get_car_damage_data(soup)
  contract_data = get_contract_data(soup)
  client_data = get_client_data(soup)

  user_claim_contact_data = car_insurance_claim_data["contact_person"].split(" ")
  if len(user_claim_contact_data) == 3:
    contact_number = user_claim_contact_data[2]
  else:
    contact_number = ""

  response = {
    "registration_number": vehicle_data["registration_number"],
    "VIN": vehicle_data["VIN"],
    "make_and_model": vehicle_data["make_and_model"],
    "phone_number": contact_number,
    "client_name": client_data["client_company_name"],
    "method_of_claim_settlement": car_insurance_claim_data["method_of_claim_settlement"],
    "insurance_policy_number": "do uzupełnienia w przyszłości",
    "insurer_name": insurance_data["insurer_name"],
    "claim_number": car_insurance_claim_data["claim_number"],
    "date_of_incident": car_insurance_claim_data["date_of_incident"],
    "description_of_incident": car_insurance_claim_data["description_of_incident"],
    "car_service_name": car_insurance_claim_data["car_service_name"],
    "car_service_address": car_insurance_claim_data["car_service_address"]
  }

  return response

def parse_html(html):
  soup = BeautifulSoup(html, "html.parser")

  alias = get_alias(soup)
  vehicle_data = get_vehicle_data(soup)
  car_insurance_claim_data = get_car_insurance_claim_data(soup)
  insurance_data = get_insurance_data(soup)
  car_damage_data = get_car_damage_data(soup)
  contract_data = get_contract_data(soup)
  client_data = get_client_data(soup)

  user_claim_contact_data = car_insurance_claim_data["contact_person"].split(" ")
  if len(user_claim_contact_data) == 3:
    contact_number = user_claim_contact_data[2]
  else:
    contact_number = ""

  if "oc" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower():
    message_title = f"{vehicle_data['registration_number']} / {alias} / OC sprawcy"
    message_header = "<b>LIKWIDACJA Z POLISY OC SPRAWCY</b><br><br>"
    message_body = f"Polisa OC - treść zlecenia;<br>kontakt do użytkownika: <b>{contact_number}</b>"
  elif (
    "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
    and ("klient" in insurance_data["insurance_source_1"].lower() or "klient" in insurance_data["insurance_source_2"].lower())
    and "efl" in client_data["client_company_name"].lower()
  ):
    message_title = f"{vehicle_data['registration_number']} / {alias} / AC EFL"
    message_header = "<b>LIKWIDACJA Z POLISY AC EFL</b><br><br>"
    message_body = f"Polisa AC Klienta - treść zlecenia;<br>kontakt do użytkownika: <b>{contact_number}</b>"
  elif (
    "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
    and ("klient" in insurance_data["insurance_source_1"].lower() or "klient" in insurance_data["insurance_source_2"].lower())
    and "optima-fleet" in str(client_data["fleet_managers_contat_details"]).lower()
  ):
    message_title = f"{vehicle_data['registration_number']} / {alias} / AC IMPEL"
    message_header = "<b>LIKWIDACJA Z POLISY AC IMPEL</b><br><br>"
    message_body = f"Polisa AC Klienta - treść zlecenia;<br>kontakt do użytkownika: <b>{contact_number}</b>"
  elif (
    "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
    and ("klient" in insurance_data["insurance_source_1"].lower() or "klient" in insurance_data["insurance_source_2"].lower())
  ):
    message_title = f"{vehicle_data['registration_number']} / {alias} / AC klienta"
    message_header = "<b>LIKWIDACJA Z POLISY AC KLIENTA</b><br><br>"
    message_body = f"Polisa AC Klienta - treść zlecenia;<br>kontakt do użytkownika: <b>{contact_number}</b>"
  elif (
    "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
    and ("carefleet" in insurance_data["insurance_source_1"].lower() or "carefleet" in insurance_data["insurance_source_2"].lower())
  ):
    insurer = insurance_data["insurer_name"].lower()
    message_title = f"{vehicle_data['registration_number']} / {alias} / AC Carefleet"
    message_body = f"Polisa AC Carefleet - treść zlecenia;<br>kontakt do użytkownika: <b>{contact_number}</b>"
    if "ergo hestia" in insurer:
      message_header = "<b>LIKWIDACJA Z POLISY AC Carefleet / Ergo Hestia</b><br><br>"
    elif "generali" in insurer:
      message_header = "<b>LIKWIDACJA Z POLISY AC Carefleet / Generali</b><br><br>"
    elif "warta" in insurer:
      message_header = "<b>LIKWIDACJA Z POLISY AC Carefleet / Warta</b><br><br>"
    elif "interrisk" in insurer:
      message_header = "<b>LIKWIDACJA Z POLISY AC Carefleet / Interrisk</b><br><br>"
    elif "powszechny" in insurer:
      message_header = "<b>LIKWIDACJA Z POLISY AC Carefleet / PZU</b><br><br>"
  else:
    message_header = "<b><style color='red'>UZUPEŁNIJ ZASADY LIKWIDACJI SZKODY RĘCZNIE!</style></b><br><br>"

  response = {
    "message_title": message_title,
    "message_header": message_header,
    "message_body": message_body
  }
  
  return response