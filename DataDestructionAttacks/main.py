# Атаки на уничтожение данных
# Иногда злоумышленники хотят сделать нечто большее, чем просто временно
# отключить пользователя, завалив его запросами, — они хотят нанести ущерб
# жертве, уничтожив или повредив информацию цели или информационные
# системы. Преступник может попытаться уничтожить данные пользователя с
# помощью атаки по уничтожению данных - например, если пользователь
# отказывается платить программе-вымогателю выкуп, который требует
# мошенник. Конечно, все причины для запуска DDoS-атак (см. Предыдущий
# раздел) также являются причинами того, что хакер может попытаться
# уничтожить чьи-либо данные.
# Атаки Wiper - это продвинутые атаки на уничтожение данных, при которых
# преступник использует вредоносное ПО для удаления данных с жесткого
# диска жертвы таким образом, что их трудно или невозможно восстановить.
# Проще говоря, если у жертвы нет резервных копий, тот, чей компьютер был
# стерт с помощью wiper, скорее всего, потеряет доступ ко всем данным и программному обеспечению, 
# которые ранее хранились на атакованном устройстве.
# Одна из зловещих форм атаки с уничтожением данных заключается в том,
# что злоумышленник не стирает данные жертвы, а тайно изменяет их таким
# образом, что данные могут нанести вред, если будут использованы жертвой,
# но жертва вряд ли будет знать, что имело место какое—либо вмешательство.
# Это обсуждается позже в разделе.

# ===================================================================================================================================================

import os
import shutil
import random

# ---------- НАСТРОЙКИ ----------
SANDBOX_DIR = "sandbox_wiper_demo"
DEMO_FILES = ["document.txt", "photo.jpg", "backup.zip", "notes.txt"]

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def setup_sandbox():
    """Создаёт тестовую среду с демо-файлами."""
    if os.path.exists(SANDBOX_DIR):
        shutil.rmtree(SANDBOX_DIR)
    os.mkdir(SANDBOX_DIR)
    for fname in DEMO_FILES:
        # Используем utf-8 для поддержки русского языка
        with open(os.path.join(SANDBOX_DIR, fname), "w", encoding = "utf-8") as f:
            f.write(f"Это содержимое файла {fname}\nВажные данные пользователя.")
    print(f"[*] Песочница создана в '{SANDBOX_DIR}' с файлами: {DEMO_FILES}\n")

def list_files():
    """Показывает текущие файлы в песочнице."""
    files = os.listdir(SANDBOX_DIR)
    print("📁 Файлы в песочнице:", files if files else "пусто")
    return files

# ---------- ТИПЫ АТАК ----------
def wiper_attack_irrecoverable():
    """Атака Wiper: полное удаление ВСЕХ файлов (имитация сложного восстановления)."""
    print("\n🔻 ВЫПОЛНЯЕТСЯ АТАКА ТИПА 'WIPER' (уничтожение данных)")
    for fname in os.listdir(SANDBOX_DIR):
        path = os.path.join(SANDBOX_DIR, fname)
        # для имитации безопасного удаления перезаписываем случайными данными
        try:
            with open(path, "wb") as f:
                f.write(os.urandom(100))
            os.remove(path)
            print(f"   - {fname}: перезаписан и удалён")
        except Exception as e:
            print(f"   - Ошибка с {fname}: {e}")
    print("❌ Данные уничтожены. Восстановление штатными средствами невозможно.")
    list_files()

def corrupt_files_silent():
    """Тайное изменение данных: добавляет вредоносный код в текстовые файлы."""
    print("\n🕵️‍♂️ ВЫПОЛНЯЕТСЯ ТАЙНАЯ МОДИФИКАЦИЯ ДАННЫХ (коррупция)")
    for fname in os.listdir(SANDBOX_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(SANDBOX_DIR, fname)
            # Используем utf-8 для чтения и записи
            with open(path, "a", encoding = "utf-8") as f:
                f.write("\n\n[ВНЕДРЕНО] rm -rf / --dangerous-command\n")
            print(f"   - {fname}: изменён (добавлен скрытый вредоносный код)")
    print("⚠️ Внешне файлы выглядят нормально, но содержимое повреждено/опасно.")
    # покажем пример
    for fname in os.listdir(SANDBOX_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(SANDBOX_DIR, fname), "r", encoding = "utf-8") as f:
                content = f.read()
                print(f"\nСодержимое {fname} (первые 300 символов):\n{content[:300]}")

def selective_delete():
    """Выборочное удаление критических файлов (например, без резервной копии)."""
    print("\n🎯 ВЫБОРОЧНАЯ АТАКА: удаление важных файлов")
    to_delete = ["backup.zip", "document.txt"]
    for fname in to_delete:
        path = os.path.join(SANDBOX_DIR, fname)
        if os.path.exists(path):
            os.remove(path)
            print(f"   - {fname} удалён")
    print("Оставшиеся файлы:", os.listdir(SANDBOX_DIR))

def ransom_simulation():
    """Симуляция атаки вымогателя с требованием выкупа."""
    print("\n💰 СИМУЛЯЦИЯ АТАКИ ВЫМОГАТЕЛЯ")
    
    # Шифруем текстовые файлы (имитация)
    encrypted_files = []
    for fname in os.listdir(SANDBOX_DIR):
        if fname.endswith(".txt"):
            path = os.path.join(SANDBOX_DIR, fname)
            with open(path, "r", encoding = "utf-8") as f:
                original = f.read()
            
            # Простое "шифрование" (только для демонстрации)
            encrypted = "🔒 ЗАШИФРОВАНО ВЫМОГАТЕЛЕМ 🔒\n" + "".join(chr(ord(c) + 1) for c in original[:50])
            with open(path, "w", encoding = "utf-8") as f:
                f.write(encrypted)
            
            encrypted_files.append(fname)
            print(f"   - {fname}: зашифрован")
    
    if encrypted_files:
        print(f"\n💀 ВАЖНО: Файлы {encrypted_files} зашифрованы!")
        print("💀 Для восстановления требуется выкуп: 0.5 BTC")
        
        response = input("\nЗаплатить выкуп? (y/n - и тогда данные будут уничтожены): ").lower()
        
        if response == 'y':
            print("✅ Вы заплатили выкуп. Данные восстановлены!")
            # Восстанавливаем файлы
            for fname in encrypted_files:
                path = os.path.join(SANDBOX_DIR, fname)
                with open(path, "w", encoding = "utf-8") as f:
                    f.write(f"Восстановленный файл {fname}\nДанные возвращены после оплаты выкупа.")
            print("   - Файлы восстановлены")
        else:
            print("❌ Вы отказались платить. Запускаем Wiper атаку...")
            wiper_attack_irrecoverable()

# ---------- ДЕМОНСТРАЦИЯ ----------
def main():
    print("=" * 60)
    print("=== ДЕМОНСТРАЦИЯ АТАК НА УНИЧТОЖЕНИЕ ДАННЫХ (учебная) ===")
    print("=" * 60)
    print("\nВНИМАНИЕ: Это образовательная программа!")
    print("Все операции производятся в изолированной папке-песочнице.")
    print("Реальные данные не пострадают.\n")
    
    while True:
        print("\nМЕНЮ:")
        print("1. Атака Wiper (безвозвратное удаление)")
        print("2. Тайная модификация данных (повреждение)")
        print("3. Выборочное удаление файлов")
        print("4. Атака вымогателя (Ransomware)")
        print("5. Показать текущие файлы в песочнице")
        print("6. Сбросить песочницу к исходному состоянию")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == '1':
            setup_sandbox()
            wiper_attack_irrecoverable()
        elif choice == '2':
            setup_sandbox()
            corrupt_files_silent()
        elif choice == '3':
            setup_sandbox()
            selective_delete()
        elif choice == '4':
            setup_sandbox()
            ransom_simulation()
        elif choice == '5':
            list_files()
        elif choice == '6':
            setup_sandbox()
            print("✅ Песочница сброшена к исходному состоянию")
            list_files()
        elif choice == '0':
            print("\nЗавершение работы. Песочница осталась в папке:", SANDBOX_DIR)
            print(f"Чтобы удалить её вручную: rmdir /s {SANDBOX_DIR} (Windows) или rm -rf {SANDBOX_DIR} (Linux/Mac)")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Убедитесь, что у вас есть права на запись в текущей директории.")