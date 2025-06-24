import json
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
from settings_log.settings import logger



def connect_to_db(db_path):
    """Підключення до бази даних SQLite."""
    try:
        conn = sqlite3.connect(db_path)
        logger.info(f"Підключення до бази даних успішне ....\n\tDB-Path: {db_path}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Помилка підключення до бази даних {db_path}:\n\t{e}")
        raise


def fetch_records(conn):
    """Отримання записів з таблиці."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_name = cursor.fetchone()[0]
        logger.info(f"Отримано назву таблиці:\n\t{table_name}")
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        logger.info(f"Отримано {len(records)} записів з бази даних.")
        return records
    except sqlite3.Error as e:
        logger.error(f"Помилка отримання записів:\n\t{e}")
        raise


def normalize_date(date_str):
    """Нормалізація дати до формату ISO YYYY-MM-DD."""
    try:
        # Спробувати розпізнати дату в різних форматах
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y", "%Y.%m.%d"):
            try:
                data = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                return data
            except ValueError:
                continue
        return None
    except Exception as e:
        logger.error(f"Помилка нормалізації дати:\n\t{e}")
        return None


def normalize_amount(amount_str):
    """Нормалізація суми до десяткового формату з двома знаками після коми."""
    try:
        amount_str = amount_str.replace(',', '.')
        return f"{float(amount_str):.2f}"
    except ValueError as e:
        logger.error(f"Помилка нормалізації суми:\n\t{e}")
        return None


def validate_account_number(account_number):
    """Перевірка номера рахунку на відповідність формату."""
    if isinstance(account_number, str) and account_number.isdigit() and 3 <= len(account_number) <= 12:
        return account_number
    else:
        logger.warning(f"Некоректний номер рахунку:\n\t{account_number}")
        return None


def clean_description(description):
    """Очищення опису: видалення зайвих пробілів і обмеження довжини до 255 символів."""
    if description:
        cleaned = ' '.join(description.split()).strip()[:255]
        return cleaned
    return None


def validate_record(record):
    """Валідація запису: перевірка дати, суми, номера рахунку та опису."""
    date, account_number, amount, description = record
    normalized_date = normalize_date(date)
    normalized_amount = normalize_amount(amount)
    valid_account_number = validate_account_number(account_number)
    cleaned_description = clean_description(description)

    if normalized_date and normalized_amount and valid_account_number:
        logger.info(f"Запис успішно валідується:\n\t{record}")
        return normalized_date, valid_account_number, normalized_amount, cleaned_description
    else:
        logger.warning(f"Некоректний запис:\n\t{record}")
        return None


def count_records(records):
    """Підрахунок кількості оброблених, успішно перетворених та відкинутих записів."""
    total_records = len(records)
    valid_records = sum(1 for record in records if validate_record(record) is not None)
    invalid_records = total_records - valid_records
    return total_records, valid_records, invalid_records


def validate_and_count(records):
    """Валідація записів та підрахунок кількості оброблених, успішно перетворених та відкинутих записів."""
    valid_records = []
    for record in records:
        validated_record = validate_record(record)
        if validated_record:
            valid_records.append(validated_record)

    total_records, valid_count, invalid_count = count_records(records)
    return valid_records, total_records, valid_count, invalid_count


def create_xml(records, output_file):
    """Створення XML-файлу з перетворених записів."""
    root = ET.Element("JournalEntries")

    for record in records:
        if record is not None:
            entry = ET.SubElement(root, "Entry")
            date_elem = ET.SubElement(entry, "Date")
            date_elem.text = record[0]
            account_elem = ET.SubElement(entry, "AccountNumber")
            account_elem.text = record[1]
            amount_elem = ET.SubElement(entry, "Amount")
            amount_elem.text = record[2]
            description_elem = ET.SubElement(entry, "Description")
            description_elem.text = record[3] if record[3] else ""

    tree = ET.ElementTree(root)
    try:
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        logger.info(f"XML-файл успішно створено:\n\t{output_file}")
    except Exception as e:
        logger.error(f"Помилка при збереженні XML-файлу:\n\t{e}")
        raise


def main():
    db_path = "tech_task/journal_entries.db"
    output_file = "output/journal_entries.xml"

    try:
        conn = connect_to_db(db_path)
        records = fetch_records(conn)

        transformed_records = []
        for record in records:
            validated_record = validate_record(record)
            if validated_record:
                transformed_records.append(validated_record)

        create_xml(transformed_records, output_file)
        valid_records, total_records, valid_count, invalid_count = validate_and_count(records)
        logger.info(f"Загальна кількість оброблених записів: {total_records}")
        logger.info(f"Кількість успішно перетворених записів: {valid_count}")
        logger.info(f"Кількість відкинутих записів: {invalid_count}")
        logger.info("ETL процес завершено ....")
        logger.info(f"XML-файл успішно створено:\n\t{output_file}")

        with open(output_file, 'r', encoding='utf-8') as file:
            # Читання XML-файлу для виводу
            xml_content = file.read()
            xml_content_json = json.dumps(ET.tostring(ET.fromstring(xml_content), encoding='unicode', method='xml'), indent=4)
            save_json_file = "output/journal_entries.json"
            with open(save_json_file, 'w', encoding='utf-8') as json_file:
                json_file.write(xml_content_json)
            logger.info(f"JSON-файл успішно створено:\n\t{save_json_file}")

    except Exception as e:
        logger.error(f"Загальна помилка: {e}")
    finally:
        if conn:
            conn.close()
            logger.info("Підключення до бази даних закрито.")



if __name__ == "__main__":
    main()
    logger.info("ETL процес завершено ....")










