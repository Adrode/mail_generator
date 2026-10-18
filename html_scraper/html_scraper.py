from bs4 import BeautifulSoup
from datetime import datetime, timedelta

try:
  def find_text_helper(element):
    return lambda text: text and element in text

  def get_alias(soup):
    return (
      soup.find("a", string=find_text_helper("Wyloguj"))
      .find_previous_sibling("b")
      .get_text(strip=True)
    )

  def get_vehicle_data(soup):
    main_table = soup.find("label", string=find_text_helper("Rodzaj nadwozia:")).find_parent("table")
    
    vehicle_data = {
      "registration_number": (
        main_table.find("td", string=find_text_helper("Nr rejestracyjny"))
        .find_next_sibling("td")
        .find("a")
        .get_text(strip=True)
      ),
      "VIN": (
        main_table.find("label", string=find_text_helper("Nr nadwozia:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "make_and_model": (
        main_table.find("label", string=find_text_helper("Pojazd:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "first_registration_date": (
        main_table.find("label", string=find_text_helper("Data pierwszej rejestracji:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      )
    }

    return vehicle_data

  def get_car_insurance_claim_data(soup):
    main_table = soup.find("label", string=find_text_helper("Sposób rozliczania:")).find_parent("table")

    car_insurance_claim_data = {
      "car_service_name": (
        main_table.find("td", string=find_text_helper("Serwis"))
        .find_next_sibling("td")
        .find("a")
        .get_text(strip=True)
      ),
      "car_service_address": (
        main_table.find("td", string=find_text_helper("Oddział:"))
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "case_number": (
        main_table.find("td", string=find_text_helper("Numer sprawy:"))
        .find_next_sibling("td")
        .find("span")
        .get_text(strip=True)
      ),
      "insurer_name": (
        main_table.find("label", string=find_text_helper("Nazwa ZU:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "claim_number": (
        main_table.find("label", string=find_text_helper("Nr szkody:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "method_of_claim_settlement": (
        main_table.find("label", string=find_text_helper("Sposób rozliczania:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "type_of_claim_damage": (
        main_table.find("label", string=find_text_helper("Typ szkody:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "date_of_incident": (
        main_table.find("label", string=find_text_helper("Data zdarzenia:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "description_of_incident": (
        main_table.find("div", string=find_text_helper("Treść zlecenia:"))
        .find_next_sibling("div")
        .get_text(strip=True)
      ),
      "contact_person": (
        main_table.find("label", string=find_text_helper("Osoba do kontaktu:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      )
    }
    
    return car_insurance_claim_data

  def get_insurance_data(soup):
    insurance_data = {
      "insurance_source_1": (
        soup.find("label", string=find_text_helper("Ubezpieczenie zakupione przez:"))
        .find_parent("td")
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      ),
      "insurance_source_2": (
        soup.find("th", string=find_text_helper("Polisa"))
        .find_parent("table")
        .find("tbody")
        .find("tr")
        .select("td")[4]
        .get_text(strip=True)
      ),
      "insurer_name": get_car_insurance_claim_data(soup)["insurer_name"]
    }

    return insurance_data

  def get_car_damage_data(soup):
    return (
      soup.find("span", string=find_text_helper("Uszkodzenia"))
      .find_parent("tr")
      .find_next_sibling("tr")
      .find_next_sibling("tr")
      .find("td")
      .get_text(strip=True)
    )

  def get_contract_data(soup):
    main_table = soup.find("td", string=find_text_helper("Data akt/zd:")).find_parent("table")
    
    check_contract_number = (
      main_table.find("td", string=find_text_helper("Umowa finansowa:"))
      .find_next_sibling("td")
      .find("a")
    )

    if check_contract_number is None:
      contract_number = (
        main_table.find("td", string=find_text_helper("Umowa finansowa:"))
        .find_next_sibling("td")
        .find("label")
      )
    else:
      contract_number = check_contract_number

    contract_data = {
      "selected_claims_handling": (
        main_table.find("td", string=find_text_helper("Zarządzanie likwidacją szkód:"))
        .find_next_sibling("td")
        .get_text(strip=True)
      ),
      "contract_status": (
        main_table.find("td", string=find_text_helper("Stauts umowy:"))
        .find_next_sibling("td")
        .get_text(strip=True)
      ),
      "contract_number": contract_number.get_text(strip=True),
      "contract_end_date": (
        main_table.find("td", string=find_text_helper("Data akt/zd:"))
        .find_next_sibling("td")
        .find("label")
        .get_text(strip=True)
      )
    }

    return contract_data

  def get_assistance_data(soup):
    main_table = soup.find("td", string=find_text_helper("Hak holowniczy:")).find_parent("table")

    assistance_data = {
      "assistance_package": (
        main_table.find("td", string=find_text_helper("Assistance z umowy:"))
        .find_next_sibling("td")
        .find("a")
        .get_text(strip=True)
      ),
      "door_to_door": (
        main_table.find("td", string=find_text_helper("Door-to-door:"))
        .find_next_sibling("td")
        .get_text(strip=True)
      )
    }

    return assistance_data

  def get_client_data(soup):
    main_table = soup.find("a", string=find_text_helper("Segment")).find_parent("table")

    client_data = {
      "user_name": (
        main_table.find("td", string=find_text_helper("Nazwa"))
        .find_next_sibling("td")
        .find("a")
        .get_text(strip=True)
      ),
      "user_location": (
        main_table.find("label", string=find_text_helper("Miasto:"))
        .find_parent("td")
        .find_next_sibling("td") 
        .find("label")
        .get_text(strip=True)
      ),
      "client_company_name": (
        main_table.find("td", string=find_text_helper("Klient:"))
        .find_next_sibling("td")
        .find("a")
        .get_text(strip=True)
      ),
      "fleet_managers_contat_details": (
        main_table.find("td", string=find_text_helper("Flotowiec:"))
        .find_next_sibling("td")
      )
    }

    return client_data

  def parse_data_for_pdf_forms(html):
    soup = BeautifulSoup(html, "html.parser")

    alias = get_alias(soup)
    vehicle_data = get_vehicle_data(soup)
    car_insurance_claim_data = get_car_insurance_claim_data(soup)
    insurance_data = get_insurance_data(soup)
    car_damage_data = get_car_damage_data(soup)
    contract_data = get_contract_data(soup)
    assistance_data = get_assistance_data(soup)
    client_data = get_client_data(soup)

    user_claim_contact_data = car_insurance_claim_data["contact_person"].split()
    if len(user_claim_contact_data) <= 2:
      contact_number = ""
    else:
      contact_number = user_claim_contact_data[-1]

    insurance_policy_number = car_insurance_claim_data["method_of_claim_settlement"].split()[-1]
    if insurance_policy_number[-1] == ")":
      insurance_policy_number = insurance_policy_number[0:-1]

    settlement_without_insurer = True if "naprawa na koszt klienta" in car_insurance_claim_data["method_of_claim_settlement"].lower() else False
  
    if "bmw" in vehicle_data["make_and_model"].lower() and "seri" in vehicle_data["make_and_model"].lower():
      make_and_model = " ".join(vehicle_data["make_and_model"].split()[:3])
    else:
      make_and_model = " ".join(vehicle_data["make_and_model"].split()[:2])

    response = {
      "case_number": car_insurance_claim_data["case_number"],
      "alias": alias,
      "car_service_name": car_insurance_claim_data["car_service_name"],
      "car_service_address": " ".join(car_insurance_claim_data["car_service_address"].split()[1:]),
      "date_of_incident": car_insurance_claim_data["date_of_incident"],
      "registration_number": vehicle_data["registration_number"],
      "make_and_model": make_and_model,
      "vin": vehicle_data["VIN"],
      "model_year": vehicle_data["first_registration_date"].split("/")[-1],
      "owner": "Klient" if "brak" in contract_data["contract_number"].lower() else "Carefleet S.A.",
      "client_name": client_data["client_company_name"],
      "phone_number": contact_number,
      "insurance_policy_number": "-" if settlement_without_insurer else insurance_policy_number,
      "claim_number": "-" if settlement_without_insurer else car_insurance_claim_data["claim_number"],
      "method_of_claim_settlement": "Naprawa na koszt klienta" if settlement_without_insurer else car_insurance_claim_data["method_of_claim_settlement"].split()[0],
      "insurer_name": "-" if settlement_without_insurer else insurance_data["insurer_name"],
      "assistance_package": assistance_data["assistance_package"],
      "replacement_vehicle_guarantee": "Tak" if assistance_data["assistance_package"] else "Nie",
      "door_to_door_service": assistance_data["door_to_door"],
      "car_damage": car_damage_data,
      "description_of_incident": car_insurance_claim_data["description_of_incident"],
      "contract_number": contract_data["contract_number"]
    }

    return response

  def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    alias = get_alias(soup)
    vehicle_data = get_vehicle_data(soup)
    car_insurance_claim_data = get_car_insurance_claim_data(soup)
    insurance_data = get_insurance_data(soup)
    contract_data = get_contract_data(soup)
    client_data = get_client_data(soup)

    user_claim_contact_data = car_insurance_claim_data["contact_person"].split()
    if len(user_claim_contact_data) <= 2:
      contact_number = ""
    else:
      contact_number = user_claim_contact_data[-1]

    if "oc" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower():
      message_title = f"{vehicle_data['registration_number']} / {alias} / OC sprawcy"
      message_header = "<b>OC SPRAWCY</b><br><br>"
      message_body = f"<br>Polisa OC - treść;<br>kontakt: <b>{contact_number}</b>"
    elif (
      "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
      and ("klient" in insurance_data["insurance_source_1"].lower() and "klient" in insurance_data["insurance_source_2"].lower())
      and "efl" in client_data["client_company_name"].lower()
    ):
      message_title = f"{vehicle_data['registration_number']} / {alias} / AC EFL"
      message_header = "<b>AC EFL</b><br><br>"
      message_body = f"<br>AC Klienta - treść;<br>kontakt: <b>{contact_number}</b>"
    elif (
      "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
      and ("klient" in insurance_data["insurance_source_1"].lower() and "klient" in insurance_data["insurance_source_2"].lower())
      and "optima-fleet" in str(client_data["fleet_managers_contat_details"]).lower()
    ):
      message_title = f"{vehicle_data['registration_number']} / {alias} / AC IMP"
      message_header = "<b>AC IMP</b><br><br>"
      message_body = f"<br>AC Klienta - treść;<br>kontakt: <b>{contact_number}</b>"
    elif (
      "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
      and ("klient" in insurance_data["insurance_source_1"].lower() and "klient" in insurance_data["insurance_source_2"].lower())
    ):
      message_title = f"{vehicle_data['registration_number']} / {alias} / AC klienta"
      message_header = "<b>AC KLIENTA</b><br><br>"
      message_body = f"<br>AC Klienta - treść;<br>kontakt: <b>{contact_number}</b>"
    elif (
      "ac" in car_insurance_claim_data["method_of_claim_settlement"][0:2].lower()
      and ("carefleet" in insurance_data["insurance_source_1"].lower() and "carefleet" in insurance_data["insurance_source_2"].lower())
    ):
      insurer = insurance_data["insurer_name"].lower()
      message_title = f"{vehicle_data['registration_number']} / {alias} / AC Carefleet"
      message_body = f"<br>AC Carefleet - treść;<br>kontakt: <b>{contact_number}</b>"
      if "ergo hestia" in insurer:
        message_header = "<b> AC Carefleet / Ergo Hestia</b><br><br>"
      elif "generali" in insurer:
        message_header = "<b>AC Carefleet / Generali</b><br><br>"
      elif "warta" in insurer:
        message_header = "<b>AC Carefleet / Warta</b><br><br>"
      elif "interrisk" in insurer:
        message_header = "<b>AC Carefleet / Interrisk</b><br><br>"
      elif "powszechny" in insurer:
        message_header = "<b>AC Carefleet / PZU</b><br><br>"
      else:
        message_title = f"{vehicle_data['registration_number']} / {alias}"
        message_header = "<b><span style='color: red;'>UZUPEŁNIJ ZASADY LIKWIDACJI SZKODY RĘCZNIE!</span></b><br><br>"
        message_body = ""
    elif (
      "naprawa na koszt klienta" in car_insurance_claim_data["method_of_claim_settlement"].lower()
    ):
      message_title = f"{vehicle_data['registration_number']} / {alias} / naprawa na koszt klienta"
      message_header = "<b>Naprawa na koszt klienta</b><br><br>"
      message_body = f"<br>Naprawa na koszt klienta - treść;<br>kontakt: <b>{contact_number}</b>"
    else:
      message_title = f"{vehicle_data['registration_number']} / {alias}"
      message_header = "<b><span style='color: red;'>UZUPEŁNIJ ZASADY LIKWIDACJI SZKODY RĘCZNIE!</span></b><br><br>"
      message_body = ""
    

    message_additional_info = []
    if datetime.strptime(contract_data["contract_end_date"], "%d-%m-%Y").date() <= datetime.now().date() + timedelta(days=60):
      message_additional_info.append(f"<b><span style='color: red;'>KONIEC KONTRAKTU: {contract_data["contract_end_date"]}</span></b><br>")
    if "nie" in contract_data["selected_claims_handling"].lower():
      message_additional_info.append(f"<b><span style='color: red;'>BEZ ZARZĄDZANIA</span></b><br>")
    if "zdany" in contract_data["contract_status"].lower():
      message_additional_info.append(f"<b><span style='color: red;'>ZDANY</span></b><br>")

    message_additional_info = " ".join(message_additional_info)

    response = {
      "message_title": message_title,
      "message_header": message_header,
      "message_additional_info": message_additional_info,
      "message_body": message_body
    }
    
    return response

except Exception as error:
  raise error