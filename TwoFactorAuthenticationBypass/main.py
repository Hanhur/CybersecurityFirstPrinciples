# Используйте многофакторную аутентификацию, но с обходным
# путем. Например, используя номер VOIP для получения текстовых
# сообщений и настраивая номер VOIP для пересылки сообщений
# нескольким сторонам по электронной почте (как это предлагается
# бесплатно, например, Google Voice).

# Логика программы
# 1. Пользователь вводит логин и пароль (первый фактор).

# 2. Генерируется OTP-код и отправляется на VOIP-номер через SMS (эмуляция через API).

# 3. VOIP-сервис автоматически пересылает SMS на несколько email-адресов — это и есть «обходной путь», так как код получают все доверенные лица.

# 4. Программа ожидает ввод кода и проверяет его.

# 5. Если код верен — доступ разрешён.

# ===================================================================================================================================================

# import os
# import random
# import smtplib
# from email.mime.text import MIMEText  # Исправлено: MIMEText, а не MimeText
# from email.mime.multipart import MIMEMultipart
# import getpass
# import time

# # Конфигурация (замените на реальные данные)
# # VOIP-номер (формат +1234567890) - для имитации приёма SMS
# VOIP_NUMBER = "+1234567890"

# # Список email для пересылки кода (обходной путь)
# FORWARD_EMAILS = [
#     "admin1@example.com",
#     "admin2@example.com",
#     "backup@example.com"
# ]

# # Данные для отправки писем (используйте App Password для Gmail)
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# SMTP_USER = "your_voip_account@gmail.com"
# SMTP_PASSWORD = "your_app_password"

# # База пользователей (в реальном проекте — хэши паролей)
# USERS_DB = {
#     "alice": "password123",
#     "bob": "securepass"
# }

# def send_sms_via_voip_api(phone_number, message):
#     """
#     Эмуляция отправки SMS на VOIP-номер через внешний API (Twilio, Google Voice etc.)
#     В реальности здесь был бы запрос к API, но для примера — печать в консоль.
#     """
#     print(f"[VOIP] SMS отправлен на {phone_number}: {message}")
#     # Здесь можно вызвать реальный API отправки SMS
#     return True

# def forward_code_to_emails(code, recipients):
#     """
#     Рассылка полученного кода на email-адреса (имитация пересылки из Google Voice).
#     В реальном Google Voice пересылка на email настраивается вручную в интерфейсе,
#     но здесь мы показываем программную эмуляцию.
#     """
#     subject = "MFA Code from VOIP Forwarding"
#     body = f"Your MFA authentication code is: {code}\nThis code was forwarded from VOIP number {VOIP_NUMBER}."
    
#     # Создаём сообщение
#     msg = MIMEText(body)  # Исправлено: MIMEText
#     msg['Subject'] = subject
#     msg['From'] = SMTP_USER
#     msg['To'] = ", ".join(recipients)

#     try:
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.send_message(msg)
#         print(f"[EMAIL] Код {code} отправлен на {', '.join(recipients)}")
#         return True
#     except Exception as e:
#         print(f"[ERROR] Ошибка отправки email: {e}")
#         return False

# def generate_otp():
#     """Генерирует 6-значный одноразовый код."""
#     return f"{random.randint(100000, 999999)}"

# def authenticate_user():
#     """Основной процесс аутентификации с MFA через VOIP + email forwarding."""
#     print("=== MFA Login (VOIP + Email Forwarding) ===\n")
    
#     # Первый фактор: логин + пароль
#     username = input("Username: ")
#     password = getpass.getpass("Password: ")
    
#     if username not in USERS_DB or USERS_DB[username] != password:
#         print("[DENIED] Неверный логин или пароль.")
#         return False
    
#     print(f"\n[OK] Пароль принят. Отправляем MFA-код на VOIP {VOIP_NUMBER}...")
    
#     # Второй фактор: генерация и отправка кода на VOIP
#     otp_code = generate_otp()
#     send_sms_via_voip_api(VOIP_NUMBER, f"Your MFA code: {otp_code}")
    
#     # Обходной путь: немедленно пересылаем код на email-адреса
#     # (имитируем настройку пересылки в VOIP-сервисе)
#     print("[FORWARD] Настроена пересылка SMS с VOIP на несколько email (обходной путь)...")
#     forward_code_to_emails(otp_code, FORWARD_EMAILS)
    
#     # Ввод кода пользователем
#     user_code = input("\nВведите MFA-код (пришёл на VOIP и по email): ")
    
#     if user_code == otp_code:
#         print("[GRANTED] Доступ разрешён. MFA пройдена через VOIP + email forwarding.")
#         return True
#     else:
#         print("[DENIED] Неверный MFA-код.")
#         return False

# if __name__ == "__main__":
#     if authenticate_user():
#         print("\n=== Добро пожаловать в систему! ===")
#     else:
#         print("\n=== Аутентификация не пройдена ===")

# ===================================================================================================================================================

# import random
# import getpass

# # Конфигурация
# VOIP_NUMBER = "+1234567890"
# FORWARD_EMAILS = ["admin1@example.com", "admin2@example.com", "backup@example.com"]

# # База пользователей
# USERS_DB = {
#     "alice": "password123",
#     "bob": "securepass"
# }

# def send_sms_via_voip_api(phone_number, message):
#     """Эмуляция отправки SMS на VOIP-номер"""
#     print(f"[VOIP] SMS отправлен на {phone_number}: {message}")
#     return True

# def forward_code_to_emails_emulation(code, recipients):
#     """Эмуляция пересылки кода на email (без реальной отправки)"""
#     print(f"[FORWARD-EMULATION] Код {code} был бы отправлен на следующие email:")
#     for email in recipients:
#         print(f"  -> {email}")
#     print("[FORWARD-EMULATION] (В реальном Google Voice пересылка настраивается в веб-интерфейсе)")
#     return True

# def generate_otp():
#     return f"{random.randint(100000, 999999)}"

# def authenticate_user():
#     print("=== MFA Login (VOIP + Email Forwarding - Demo Mode) ===\n")
    
#     username = input("Username: ")
#     password = getpass.getpass("Password: ")
    
#     if username not in USERS_DB or USERS_DB[username] != password:
#         print("[DENIED] Неверный логин или пароль.")
#         return False
    
#     print(f"\n[OK] Пароль принят. Отправляем MFA-код на VOIP {VOIP_NUMBER}...")
    
#     otp_code = generate_otp()
#     send_sms_via_voip_api(VOIP_NUMBER, f"Your MFA code: {otp_code}")
    
#     print("[FORWARD] Настроена пересылка SMS с VOIP на несколько email (обходной путь)...")
#     forward_code_to_emails_emulation(otp_code, FORWARD_EMAILS)
    
#     print(f"\n[DEMO] Сгенерированный код: {otp_code}")  # Для демонстрации
#     user_code = input("Введите MFA-код: ")
    
#     if user_code == otp_code:
#         print("[GRANTED] Доступ разрешён.")
#         return True
#     else:
#         print("[DENIED] Неверный MFA-код.")
#         return False

# if __name__ == "__main__":
#     if authenticate_user():
#         print("\n=== Добро пожаловать в систему! ===")
#     else:
#         print("\n=== Аутентификация не пройдена ===")

# ===================================================================================================================================================

import random
import smtplib
import getpass
from email.mime.text import MIMEText

# ==================== КОНФИГУРАЦИЯ ====================

# VOIP-номер (формат +1234567890) - для имитации приёма SMS
VOIP_NUMBER = "+1234567890"

# Список email для пересылки кода (обходной путь)
FORWARD_EMAILS = [
    "admin1@example.com",
    "admin2@example.com",
    "backup@example.com"
]

# Данные для отправки писем (только для РЕАЛЬНОГО режима)
# Для Gmail используйте пароль приложения: https://myaccount.google.com/apppasswords
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_voip_account@gmail.com"
SMTP_PASSWORD = "your_app_password"

# База пользователей (в реальном проекте — хэши паролей)
USERS_DB = {
    "alice": "password123",
    "bob": "securepass"
}

# Режим работы: "real" - реальная отправка email, "demo" - эмуляция
MODE = "demo"  # Измените на "real" для реальной отправки

# ==================== ФУНКЦИИ ====================

def send_sms_via_voip_api(phone_number, message):
    """
    Эмуляция отправки SMS на VOIP-номер через внешний API
    В реальности здесь был бы запрос к API (Twilio, Google Voice etc.)
    """
    print(f"[VOIP] SMS отправлен на {phone_number}: {message}")
    print(f"[VOIP] Сообщение: {message}")
    return True

def forward_code_to_emails_real(code, recipients):
    """Реальная отправка кода на email через SMTP"""
    subject = "MFA Code from VOIP Forwarding"
    body = f"Your MFA authentication code is: {code}\nThis code was forwarded from VOIP number {VOIP_NUMBER}."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[EMAIL] ✅ Код {code} успешно отправлен на {', '.join(recipients)}")
        return True
    except Exception as e:
        print(f"[ERROR] ❌ Ошибка отправки email: {e}")
        print(f"[HINT] Проверьте SMTP_USER, SMTP_PASSWORD и настройки безопасности Gmail")
        return False

def forward_code_to_emails_demo(code, recipients):
    """Эмуляция пересылки кода на email (без реальной отправки)"""
    print(f"[FORWARD-EMULATION] 🔄 Код {code} был бы отправлен на следующие email:")
    for email in recipients:
        print(f"  📧 -> {email}")
    print("[FORWARD-EMULATION] 💡 В реальном Google Voice пересылка настраивается в веб-интерфейсе")
    print("[FORWARD-EMULATION] 💡 Или используйте MODE='real' для реальной отправки")
    return True

def forward_code_to_emails(code, recipients):
    """Маршрутизатор: выбирает режим работы (реальный или демо)"""
    if MODE == "real":
        return forward_code_to_emails_real(code, recipients)
    else:
        return forward_code_to_emails_demo(code, recipients)

def generate_otp():
    """Генерирует 6-значный одноразовый код"""
    return f"{random.randint(100000, 999999)}"

def authenticate_user():
    """Основной процесс аутентификации с MFA через VOIP + email forwarding"""
    print("=" * 60)
    print("=== MFA Login (VOIP + Email Forwarding) ===")
    print(f"=== Режим: {'🔐 РЕАЛЬНЫЙ (отправка email)' if MODE == 'real' else '🎮 ДЕМО-РЕЖИМ (эмуляция)'} ===")
    print("=" * 60)
    print()
    
    # Первый фактор: логин + пароль
    username = input("👤 Username: ")
    password = getpass.getpass("🔒 Password: ")
    
    if username not in USERS_DB or USERS_DB[username] != password:
        print("\n❌ [DENIED] Неверный логин или пароль.")
        return False
    
    print(f"\n✅ [OK] Пароль принят.")
    print(f"📱 Отправляем MFA-код на VOIP {VOIP_NUMBER}...")
    
    # Второй фактор: генерация и отправка кода на VOIP
    otp_code = generate_otp()
    send_sms_via_voip_api(VOIP_NUMBER, f"Your MFA code: {otp_code}")
    
    # Обходной путь: пересылаем код на email-адреса
    print("\n🔄 [FORWARD] Настроена пересылка SMS с VOIP на несколько email (обходной путь)...")
    forward_code_to_emails(otp_code, FORWARD_EMAILS)
    
    # Для демо-режима показываем код (чтобы было удобно тестировать)
    if MODE == "demo":
        print(f"\n🎮 [DEMO] Сгенерированный код для тестирования: {otp_code}")
    
    # Ввод кода пользователем
    print()
    user_code = input("🔑 Введите MFA-код (пришёл на VOIP и по email): ")
    
    if user_code == otp_code:
        print("\n✅ [GRANTED] Доступ разрешён. MFA пройдена через VOIP + email forwarding.")
        return True
    else:
        print("\n❌ [DENIED] Неверный MFA-код.")
        return False

def show_configuration():
    """Показывает текущую конфигурацию"""
    print("\n" + "=" * 60)
    print("📋 ТЕКУЩАЯ КОНФИГУРАЦИЯ")
    print("=" * 60)
    print(f"VOIP номер: {VOIP_NUMBER}")
    print(f"Email для пересылки: {', '.join(FORWARD_EMAILS)}")
    print(f"Режим работы: {'РЕАЛЬНЫЙ' if MODE == 'real' else 'ДЕМО (эмуляция)'}")
    if MODE == "real":
        print(f"SMTP сервер: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"SMTP пользователь: {SMTP_USER}")
    print("=" * 60)

def main():
    """Главная функция программы"""
    show_configuration()
    
    print("\n🚀 ЗАПУСК АУТЕНТИФИКАЦИИ\n")
    
    if authenticate_user():
        print("\n" + "=" * 60)
        print("🎉 ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ!")
        print("=" * 60)
        print("✅ Аутентификация успешно пройдена")
        print("🔐 Уровень доступа: ПОЛНЫЙ")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⛔ ДОСТУП ЗАПРЕЩЁН")
        print("=" * 60)
        print("❌ Аутентификация не пройдена")
        print("=" * 60)

if __name__ == "__main__":
    main()