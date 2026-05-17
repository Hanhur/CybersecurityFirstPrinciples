# Атаки с использованием искаженного URL: Атаки с использованием
# искаженного URL-адреса - это атаки, при которых злоумышленник
# создает URL-адрес, который выглядит как ссылка на определенный
# законный веб-сайт, но из-за специальных символов, используемых в
# тексте URL-адреса, на самом деле совершает что-то гнусное. Затем
# злоумышленник может распространить вредоносный URL-адрес в
# электронной почте и текстовых сообщениях или разместив его в
# комментарии в блоге или через другие социальные сети.
# Другая форма атаки с искаженным URL-адресом - это атака, при которой
# злоумышленник создает URL-адрес, содержащий в себе элементы,
# которые приведут к сбою в работе системы, к которой осуществляется доступ.

# ===================================================================================================================================================

import re
import urllib.parse
from typing import Dict, List, Tuple

class URLPhishingDetector:
    """Класс для обнаружения и анализа искажённых URL."""
    
    def __init__(self):
        # Паттерны подозрительных конструкций
        self.suspicious_patterns = [
            (r'@', "Символ '@' может указывать на подмену домена (например, http://легитимный.com@вредоносный.ru)"),
            (r'%[0-9A-Fa-f]{2}', "URL-кодирование (%XX) может скрывать настоящий адрес"),
            (r'(?i)(xn--)', "Международные домены (Punycode) могут имитировать известные сайты (homograph attack)"),
            (r'[Ａ-Ｚａ-ｚ０-９]', "Широкие символы (fullwidth) — попытка визуального обмана"),
            (r'\\u[0-9A-Fa-f]{4}', "Экранирование Unicode может быть использовано для обфускации"),
            (r'\.{2,}', "Множественные точки в домене (например, google..com)"),
            (r'[?&][^=]+=[^&]*$', "Подозрительные параметры без чёткого значения"),
        ]
        
        # Известные легитимные домены (для примера)
        self.trusted_domains = {"google.com", "yandex.ru", "github.com", "python.org"}
    
    def detect_obfuscation(self, url: str) -> List[Tuple[str, str]]:
        """
        Проверяет URL на признаки искажения.
        Возвращает список найденных проблем с описанием.
        """
        warnings = []
        decoded_url = urllib.parse.unquote(url)  # декодируем %XX
        
        for pattern, description in self.suspicious_patterns:
            if re.search(pattern, url) or re.search(pattern, decoded_url):
                warnings.append((pattern, description))
        
        # Проверка на скрытый редирект через @
        if '@' in url and url.count('@') == 1:
            parts = url.split('@')
            if len(parts) == 2 and '//' in parts[0]:
                warnings.append(('@редирект', f"Возможный фишинг: реальный хост — {parts[1].split('/')[0]}"))
        
        # Проверка на слишком длинный URL (DoS-сценарий)
        if len(url) > 2000:
            warnings.append(('length', f"Чрезмерная длина URL ({len(url)} символов) может вызвать сбой"))
        
        return warnings
    
    def extract_real_domain(self, url: str) -> str:
        """Пытается извлечь настоящий домен из искажённого URL."""
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc
        
        # Если есть @, берём часть после последнего @
        if '@' in netloc:
            netloc = netloc.split('@')[-1]
        elif '@' in url and '//' in url:
            # Обработка случаев вида http://легитимный@вредоносный
            after_scheme = url.split('//', 1)[1] if '//' in url else url
            if '@' in after_scheme:
                netloc = after_scheme.split('@', 1)[1].split('/', 1)[0]
        
        return netloc.split(':')[0]  # убираем порт
    
    def is_phishing_attempt(self, url: str) -> Tuple[bool, str]:
        """
        Определяет, является ли URL подозрительным на фишинг.
        Возвращает (подозрение, пояснение).
        """
        real_domain = self.extract_real_domain(url)
        warnings = self.detect_obfuscation(url)
        
        # Если реальный домен не в доверенных, а есть обфускация — тревога
        if warnings and real_domain not in self.trusted_domains:
            if any(pat[0] in ['@', '%[0-9A-Fa-f]{2}', '(?i)(xn--)'] for pat, _ in warnings[:2]):
                return True, f"Фишинг! Реальный домен: {real_domain}. Признаки: {[desc for _, desc in warnings[:2]]}"
        
        if len(warnings) >= 2:
            return True, f"Высокая вероятность атаки. Домен: {real_domain}. Обнаружено: {len(warnings)} признаков искажения."
        
        return False, "Визуально подозрений нет, но требуется ручная проверка." if warnings else "URL выглядит легитимно."


class MalformedURLAttackSimulator:
    """Симуляция создания URL, способных вызвать сбой системы."""
    
    @staticmethod
    def create_buffer_overflow_url(base_url: str) -> str:
        """Создаёт очень длинный URL для тестирования устойчивости."""
        long_param = "A" * 5000
        return f"{base_url}?overflow={long_param}"
    
    @staticmethod
    def create_null_byte_url(base_url: str) -> str:
        """Вставляет %00 (null byte) для попытки обмана парсера."""
        return f"{base_url}%00.php?param=value"
    
    @staticmethod
    def create_bad_encoding_url() -> str:
        """Некорректное URL-кодирование, которое может вызвать ошибку."""
        return "http://example.com/%ZZ%s%"
    
    @staticmethod
    def generate_obfuscated_phishing_url(legitimate_domain: str, malicious_ip: str) -> str:
        """Создаёт искажённый URL: http://легитимный@IP-адрес"""
        return f"http://{legitimate_domain}@{malicious_ip}/login"
    
    @staticmethod
    def generate_homograph_attack(domain: str) -> str:
        """Пример: замена 'a' на символ из кириллицы (визуально похож)."""
        # В реальности используйте IDNA (punycode), здесь — демонстрация
        homograph = domain.replace('a', 'а')  # латинская 'a' на кириллическую 'а'
        return f"http://{homograph}.com"


def demo_attacks():
    """Демонстрация работы программы."""
    detector = URLPhishingDetector()
    simulator = MalformedURLAttackSimulator()
    
    test_urls = [
        "http://google.com@evil.ru/login",  # классический фишинг через @
        "http://www.google.com%2F%2Fevil.com",  # кодированный URL
        "http://аррӏе.com",  # homograph (буквы заменены)
        "http://xn--80ak6aa92e.com/",  # punycode для вредоносного домена
        "http://python.org",  # безопасный
        "https://github.com" + "A"*3000,  # слишком длинный
        "http://example.com/%00admin",  # null byte
        simulator.generate_obfuscated_phishing_url("paypal.com", "192.168.1.100"),
    ]
    
    print("=== Анализ подозрительных URL ===\n")
    for url in test_urls:
        print(f"URL: {url[:100]}{'...' if len(url) > 100 else ''}")
        warnings = detector.detect_obfuscation(url)
        if warnings:
            print("  [!] Обнаружены признаки искажения:")
            for _, desc in warnings:
                print(f"      - {desc}")
        
        is_phish, msg = detector.is_phishing_attempt(url)
        print(f"  [>] Вердикт: {msg}\n")
    
    print("\n=== Симуляция DoS-сбоя (атака искажённым URL) ===")
    crash_url = simulator.create_buffer_overflow_url("http://target-site.com/login")
    print(f"Создан URL для переполнения буфера: {crash_url[:150]}... (длина: {len(crash_url)} символов)")
    print("Такие URL в реальных системах могут вызывать падение парсера или веб-сервера.")
    
    print("\n=== Атака null byte ===")
    null_url = simulator.create_null_byte_url("http://site.com/admin")
    print(f"Сгенерирован URL с null-байтом: {null_url}")
    print("Некоторые старые системы обрезают строку на %00, что позволяет обойти проверки расширений.")


if __name__ == "__main__":
    demo_attacks()