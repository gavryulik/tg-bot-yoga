import gspread
from oauth2client.service_account import ServiceAccountCredentials
import ssl
import urllib3

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context

# link to Google Sheets
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Yoga crm").worksheet("Schedule")


def normalize_time(t):
    if not t:
        return ""
    t = str(t).strip()
    
    if ':' in t:
        hour = t.split(':')[0].strip()
    else:
        hour = t.strip()
    
    try:
        hour_int = int(hour)
        return f"{hour_int:02d}:00"
    except ValueError:
        return t 


def get_available_days(service_name, format_type):
    all_records = sheet.get_all_records()
    days = set()
    
    for r in all_records:
        rec_service = str(r.get('service', '')).strip()
        rec_format = str(r.get('format', '')).strip()
        rec_day = str(r.get('day', '')).strip()
        rec_status = str(r.get('status', '')).strip().lower()

        if rec_format.lower() in ["групове", "группа", "group", "груповий"]:
            normalized_format = "Групове"
        else:
            normalized_format = rec_format

        if (rec_service == service_name and
            normalized_format == format_type and
            rec_status == "вільно"):
            
            clean_day = rec_day.replace(" ", "").replace("\n", "").strip()
            days.add(clean_day)

    order = {"Понеділок": 1, "Вівторок": 2, "Середа": 3, "Четвер": 4,
             "П'ятниця": 5, "Субота": 6, "Неділя": 7}
    
    sorted_days = sorted(list(days), key=lambda x: order.get(x, 99))
    print(f"DEBUG: Знайдені дні для {format_type}: {sorted_days}")
    return sorted_days


def get_available_times(service_name, format_type, day):
    all_records = sheet.get_all_records()
    times = set()
    
    for r in all_records:
        if (str(r.get('service', '')).strip() == service_name and
            str(r.get('day', '')).strip() == day):
            
            rec_format = str(r.get('format', '')).strip()
            status = str(r.get('status', '')).strip().lower()
            spots = int(r.get('вільні місця', 0) or 0)

            if rec_format == format_type or \
               (rec_format.lower() in ["групове", "группа", "group"] and format_type == "Групове"):
                
                if format_type == "Групове":
                    if spots > 0:
                        times.add(normalize_time(r.get('time')))
                else:
                    if status == "вільно":
                        times.add(normalize_time(r.get('time')))
    
    return sorted(list(times))


def save_to_gsheet(data):
    if data.get('chosen_yoga') == "Sound Healing":
        print("✅ Sound Healing заявка прийнята (без таблиці)")
        return True

    all_records = sheet.get_all_records()
    target_service = data['chosen_yoga'].strip()
    target_format = data['format'].strip()
    target_day = data['day'].strip()
    target_time = normalize_time(data['time'])

    row_index = 0
    current_spots = 0

    for i, record in enumerate(all_records):
        rec_service = str(record.get('service', '')).strip()
        rec_format = str(record.get('format', '')).strip()
        rec_day = str(record.get('day', '')).strip()
        rec_time = normalize_time(record.get('time', ''))

        if (rec_service == target_service and
            rec_format == target_format and
            rec_day == target_day and
            rec_time == target_time):
            
            row_index = i + 2
            current_spots = int(record.get('вільні місця', 0) or 0)
            break

    if row_index == 0:
        print("❌ Слот не знайдено!")
        return False

    new_entry = f"Ім'я: {data['name']}, Тел: {data['phone']}"

    if target_format == "Групове":
        if current_spots <= 0:
            print("❌ Місць немає!")
            return False

        new_spots = current_spots - 1
        sheet.update_cell(row_index, 9, new_spots)

        existing = str(sheet.cell(row_index, 10).value or "")
        updated_text = existing + "\n" + new_entry if existing else new_entry
        sheet.update_cell(row_index, 10, updated_text)

        if new_spots <= 0:
            sheet.update_cell(row_index, 6, "зайнято")

        print(f"✅ Групове: записано. Залишилось місць: {new_spots}")
    else:
        sheet.update_cell(row_index, 6, "зайнято")
        sheet.update_cell(row_index, 7, data['name'])
        sheet.update_cell(row_index, 8, data['phone'])
        print(f"✅ Індивідуальне: записано в рядок {row_index}")

    return True