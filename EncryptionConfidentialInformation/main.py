# Храните все конфиденциальные данные в зашифрованном формате. Если у
# вас есть сомнения относительно того, является ли что-то достаточно
# конфиденциальным, чтобы требовать шифрования, вероятно, так оно и есть,
# поэтому проявите осторожность и зашифруйте.
# Шифрование встроено во многие версии Windows, а также доступно
# множество бесплатных инструментов шифрования. Удивительно, сколько
# конфиденциальных данных, которые были скомпрометированы, могли бы
# оставаться в безопасности, если бы стороны, у которых они были украдены,
# использовали бесплатные инструменты шифрования.
# Кроме того, никогда не передавайте конфиденциальную информацию, если
# она не зашифрована. Никогда не вводите конфиденциальную информацию на
# какой-либо веб-сайт, если сайт не использует шифрование TLS (этот тип
# шифрования иногда называют SSL, хотя протокол SSL был заменен на TLS
# много лет назад), о чем свидетельствует загрузка страницы по протоколу
# HTTPS, а не HTTP, разницу легко увидеть, просмотрев строку URL в веббраузере. Шифрование включает в себя сложные математические алгоритмы,
# но вам не нужно знать никаких деталей, чтобы использовать шифрование и
# извлекать из него выгоду. Однако имейте в виду, что эпоха квантовых вычислений, то есть
# новых устройств (мы называем их “компьютерами”, потому что у нас
# пока нет для них лучшего термина), которые используют квантовую
# физику для хранения данных и выполнения вычислений, а не биты,
# состоящие строго из 0 или 1, вероятно, сделает многие современные
# механизмы шифрования устаревшими и сделает данные, зашифрованные
# с помощью современных технологий, уязвимыми для взлома. Как скоро
# наступит такое так называемое “квантовое превосходство”, неизвестно, и
# эксперты придерживаются совершенно разных мнений относительно
# того, сколько лет это займет. Итак, обратите внимание на обновления,
# предлагаемые поставщиками, которые гарантируют, что их продукты
# “квантово безопасны” — некоторые такие обновления уже доступны. Также имейте в виду два основных семейства алгоритмов шифрования,
# которые используются сегодня (в дополнение к появляющимся якобы
# “квантово безопасным” механизмам шифрования). Симметричный: Вы используете один и тот же секретный ключ для
# шифрования и дешифрования.
# Асимметричный: Вы используете один секретный ключ для
# шифрования, а другой - для дешифрования. (Это тип, которому квантовые
# вычисления угрожают больше всего.) Большинство простых инструментов шифрования используют симметричное
# шифрование, и все, что вам нужно запомнить, - это пароль для расшифровки
# ваших данных. Однако на протяжении вашей профессиональной карьеры вы
# можете сталкиваться с различными асимметричными системами, которые
# требуют от вас создания как открытого, так и закрытого ключа. Открытый
# ключ доступен всему миру, а закрытый ключ хранится в секрете.
# Асимметричное шифрование помогает при отправке данных:
# Если вы хотите отправить информацию Джону так, чтобы только Джон
# мог ее прочитать, зашифруйте данные открытым ключом Джона, чтобы
# только Джон мог их прочитать, потому что он единственный участник, у
# которого есть закрытый ключ Джона.
# Если вы хотите отправить информацию Джону и хотите, чтобы Джон
# знал, что вы ее отправили, зашифруйте данные вашим собственным
# закрытым ключом, и, следовательно, Джон расшифрует их с помощью
# вашего открытого ключа и будет знать, что вы их отправили, потому что
# только у вас есть закрытый ключ, который идет вместе с вашим открытым
# ключом. Если вы хотите отправить информацию Джону в формате, который может
# прочитать только Джон, и в формате, в котором Джон будет знать, что вы
# ее отправили, зашифруйте ее как вашим собственным закрытым ключом,
# так и открытыми ключами Джона.
# На самом деле, поскольку асимметричность требует больших затрат
# процессора, она редко используется для шифрования целых разговоров, а
# скорее используется для шифрования специальных сеансовых ключей, то есть
# для передачи участникам разговора ключей, которые им необходимы для
# симметричного шифрования. Последующие коммуникации между сторонами
# осуществляются с использованием симметричного шифрования с
# использованием ключей, надежно передаваемых с использованием
# асимметричного шифрования.

# ===================================================================================================================================================

"""
Безопасное хранилище конфиденциальных данных
с поддержкой симметричного и асимметричного шифрования
"""

import os
import base64
import json
from getpass import getpass
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend


class SecureStorage:
    """
    Класс для безопасного хранения конфиденциальных данных.
    Использует симметричное шифрование (Fernet / AES) для данных "в покое".
    """
    
    def __init__(self, storage_path = "secure_storage.json"):
        self.storage_path = storage_path
        self.key = None  # симметричный ключ (будет получен из пароля)
        self.fernet = None
        
    def _derive_key_from_password(self, password: bytes, salt: bytes = None):
        """Получение ключа из пароля с использованием PBKDF2 (устойчиво к перебору)"""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = salt,
            iterations = 100_000,
            backend = default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key, salt
    
    def create_new_vault(self, password: str):
        """Создание нового защищённого хранилища"""
        key, salt = self._derive_key_from_password(password.encode())
        self.key = key
        self.fernet = Fernet(self.key)
        # Сохраняем соль для последующего восстановления ключа
        empty_vault = {
            "salt": base64.b64encode(salt).decode(),  # bytes -> string
            "data": self.fernet.encrypt(json.dumps({}).encode()).decode()  # bytes -> string
        }
        self._save_vault(empty_vault)
        print("✅ Новое защищённое хранилище создано.")
        
    def unlock(self, password: str):
        """Разблокировка хранилища с паролем"""
        try:
            with open(self.storage_path, "r") as f:
                vault = json.load(f)
            salt = base64.b64decode(vault["salt"])  # string -> bytes
            key, _ = self._derive_key_from_password(password.encode(), salt)
            fernet = Fernet(key)
            # Проверяем, что ключ правильный — пытаемся расшифровать
            encrypted_data = vault["data"].encode()  # string -> bytes
            fernet.decrypt(encrypted_data)
            self.key = key
            self.fernet = fernet
            print("🔓 Хранилище разблокировано.")
            return True
        except Exception as e:
            print(f"❌ Ошибка: неверный пароль или повреждённое хранилище.")
            return False
    
    def _save_vault(self, vault):
        with open(self.storage_path, "w") as f:
            json.dump(vault, f, indent = 2)
    
    def _load_decrypted_data(self) -> dict:
        """Загружает и расшифровывает данные"""
        with open(self.storage_path, "r") as f:
            vault = json.load(f)
        encrypted_data = vault["data"].encode()  # string -> bytes
        decrypted = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted)
    
    def _save_encrypted_data(self, data: dict):
        """Шифрует и сохраняет данные"""
        with open(self.storage_path, "r") as f:
            vault = json.load(f)
        # Шифруем и преобразуем bytes в string для JSON
        encrypted_bytes = self.fernet.encrypt(json.dumps(data).encode())
        vault["data"] = encrypted_bytes.decode()  # bytes -> string
        with open(self.storage_path, "w") as f:
            json.dump(vault, f, indent = 2)
    
    def add_secret(self, key: str, value: str):
        """Добавить конфиденциальные данные (всегда шифруются)"""
        if not self.fernet:
            print("❌ Хранилище не разблокировано.")
            return
        data = self._load_decrypted_data()
        data[key] = value
        self._save_encrypted_data(data)
        print(f"🔐 Секрет '{key}' сохранён в зашифрованном виде.")
    
    def get_secret(self, key: str) -> str:
        """Получить конфиденциальные данные (только для авторизованного доступа)"""
        if not self.fernet:
            print("❌ Хранилище не разблокировано.")
            return None
        data = self._load_decrypted_data()
        return data.get(key, None)
    
    def list_secrets(self):
        """Показать только названия ключей (сами значения скрыты)"""
        if not self.fernet:
            print("❌ Хранилище не разблокировано.")
            return
        data = self._load_decrypted_data()
        print("📋 Список сохранённых секретов (скрыто):")
        for k in data.keys():
            print(f"  - {k}")


class AsymmetricDemo:
    """
    Демонстрация асимметричного шифрования для передачи сессионных ключей
    и цифровой подписи.
    """
    
    @staticmethod
    def generate_key_pair():
        """Генерация пары ключей RSA (асимметричное шифрование)"""
        private_key = rsa.generate_private_key(
            public_exponent = 65537,
            key_size = 2048,
            backend = default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    @staticmethod
    def encrypt_with_public_key(public_key, message: bytes) -> bytes:
        """Шифрование сообщения открытым ключом (только получатель расшифрует)"""
        return public_key.encrypt(
            message,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
    
    @staticmethod
    def decrypt_with_private_key(private_key, ciphertext: bytes) -> bytes:
        """Расшифровка закрытым ключом"""
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf = padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
    
    @staticmethod
    def sign_with_private_key(private_key, message: bytes) -> bytes:
        """Цифровая подпись сообщения (подтверждение авторства)"""
        return private_key.sign(
            message,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length = padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    @staticmethod
    def verify_with_public_key(public_key, message: bytes, signature: bytes) -> bool:
        """Проверка подписи открытым ключом"""
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf = padding.MGF1(hashes.SHA256()),
                    salt_length = padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def secure_session_key_exchange():
        """
        Демонстрация: Алиса и Боб обмениваются симметричным ключом через асимметричное шифрование.
        Так работает TLS/HTTPS.
        """
        print("\n🔁 Демонстрация безопасной передачи симметричного ключа:")
        
        # Генерация ключей Боба (сервер)
        bob_private, bob_public = AsymmetricDemo.generate_key_pair()
        
        # Алиса генерирует сессионный ключ для симметричного шифрования
        session_key = Fernet.generate_key()
        print(f"🔑 Алиса создала сессионный ключ (симметричный): {session_key[:10]}... (скрыто)")
        
        # Алиса шифрует сессионный ключ открытым ключом Боба
        encrypted_session_key = AsymmetricDemo.encrypt_with_public_key(bob_public, session_key)
        print("📦 Алиса зашифровала сессионный ключ открытым ключом Боба.")
        
        # Боб расшифровывает своим закрытым ключом
        decrypted_key = AsymmetricDemo.decrypt_with_private_key(bob_private, encrypted_session_key)
        print(f"🔓 Боб расшифровал сессионный ключ: {decrypted_key[:10]}... (совпадает)")
        
        # Теперь оба могут использовать симметричное шифрование (быстро)
        fernet_alice = Fernet(session_key)
        fernet_bob = Fernet(decrypted_key)
        # Используем латиницу для байтовой строки
        message = b"Confidential conversation content"
        encrypted_msg = fernet_alice.encrypt(message)
        decrypted_msg = fernet_bob.decrypt(encrypted_msg)
        print(f"💬 Симметричное сообщение после расшифровки: {decrypted_msg.decode()}")
        print("✅ Вывод: асимметричное шифрование защитило передачу симметричного ключа.")
        
    @staticmethod
    def digital_signature_demo():
        """Демонстрация подписи сообщения закрытым ключом"""
        print("\n🖊️ Демонстрация цифровой подписи:")
        alice_private, alice_public = AsymmetricDemo.generate_key_pair()
        # Используем латиницу для байтовой строки
        message = b"Important message from Alice"
        signature = AsymmetricDemo.sign_with_private_key(alice_private, message)
        print(f"📝 Алиса подписала сообщение своим закрытым ключом.")
        
        # Боб проверяет подпись открытым ключом Алисы
        is_valid = AsymmetricDemo.verify_with_public_key(alice_public, message, signature)
        print(f"✅ Боб проверил подпись: {'Подпись верна, сообщение от Алисы' if is_valid else 'Подпись недействительна'}")
        

def main():
    print("=" * 60)
    print("🛡️ БЕЗОПАСНОЕ ХРАНИЛИЩЕ КОНФИДЕНЦИАЛЬНЫХ ДАННЫХ")
    print("=" * 60)
    print("⚠️ ВНИМАНИЕ: В эпоху квантовых вычислений современное шифрование может стать уязвимым.")
    print("Рекомендуется следить за 'квантово-безопасными' обновлениями.\n")
    
    storage = SecureStorage()
    
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Создать новое защищённое хранилище")
        print("2. Разблокировать существующее хранилище")
        print("3. Добавить секрет (шифруется)")
        print("4. Получить секрет")
        print("5. Показать все ключи секретов")
        print("6. Демонстрация асимметричного шифрования (TLS/сессионные ключи)")
        print("7. Демонстрация цифровой подписи")
        print("8. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            pwd = getpass("Придумайте надёжный пароль: ")
            confirm = getpass("Повторите пароль: ")
            if pwd == confirm:
                storage.create_new_vault(pwd)
            else:
                print("❌ Пароли не совпадают.")
        
        elif choice == "2":
            pwd = getpass("Введите пароль: ")
            storage.unlock(pwd)
        
        elif choice == "3":
            if not storage.fernet:
                print("❌ Сначала разблокируйте хранилище (пункт 2).")
                continue
            secret_key = input("Название секрета (например, 'api_key'): ")
            secret_value = getpass("Значение секрета (не будет отображаться): ")
            storage.add_secret(secret_key, secret_value)
        
        elif choice == "4":
            if not storage.fernet:
                print("❌ Сначала разблокируйте хранилище.")
                continue
            secret_key = input("Название секрета: ")
            value = storage.get_secret(secret_key)
            if value:
                print(f"🔓 Значение: {value}")
            else:
                print("❌ Секрет не найден.")
        
        elif choice == "5":
            storage.list_secrets()
        
        elif choice == "6":
            AsymmetricDemo.secure_session_key_exchange()
        
        elif choice == "7":
            AsymmetricDemo.digital_signature_demo()
        
        elif choice == "8":
            print("🔒 Выход. Пожалуйста, храните пароль в безопасности.")
            break
        
        else:
            print("❌ Неверный выбор.")


if __name__ == "__main__":
    main()