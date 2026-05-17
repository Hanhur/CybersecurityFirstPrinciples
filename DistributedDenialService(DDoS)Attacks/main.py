# Распределенные атаки типа "отказ в обслуживании" (DDoS)
# Распределенная атака типа "отказ в обслуживании" (DDoS) - это DoS-атака,
# при которой множество отдельных компьютеров или других подключенных
# устройств в разных регионах одновременно засыпают цель запросами. В
# последние годы почти все крупные атаки типа "отказ в обслуживании"
# носили распределенный характер, а в некоторых в качестве средств атаки
# использовались подключенные к Интернету камеры и другие устройства, а не
# классические компьютеры иллюстрирует анатомию простой
# DDoS-атаки. Цель DDoS-атаки - отключить жертву от сети, и мотивация для этого
# различна. Иногда цель носит финансовый характер: представьте, например,
# ущерб, который может нанести бизнесу онлайн-ритейлера, если
# недобросовестный конкурент отключит сайт ритейлера в выходные дни
# Черной пятницы. Представьте себе мошенника, который сокращает запасы
# крупного розничного продавца игрушек прямо перед тем, как начать DDoSатаку против розничного продавца за две недели до Рождества. 
# DDoS-атаки остаются серьезной и растущей угрозой. Криминальные
# структуры даже предлагают услуги DDoS-атак по найму, которые
# рекламируются в темной паутине как предложение за определенную плату
# “перевести веб-сайты ваших конкурентов в автономный режим экономически
# эффективным способом”. В некоторых случаях средства запуска DDoS-атак могут иметь политические,
# а не финансовые мотивы. Например, коррумпированные политики могут
# добиваться закрытия веб-сайтов своих оппонентов во время предвыборного
# сезона, тем самым ограничивая возможности конкурентов распространять
# сообщения и получать материалы для онлайн-кампании. Хактивисты также
# могут запускать DDoS-атаки с целью отключения сайтов во имя
# ”справедливости" — например, нападая на сайты правоохранительных
# органов после того, как во время стычки с полицией был убит безоружный
# человек, или пытаясь перевести розничного продавца в автономный режим
# после того, как этот розничный торговец поддержал дело, против которого
# выступают злоумышленники.
# DDoS-атаки могут повлиять на отдельных людей тремя существенными
# способами: DDoS-атака на локальную сеть может значительно замедлить весь
# доступ в Интернет, исходящий из этой сети. Иногда эти атаки делают
# подключение настолько медленным, что соединения с сайтами
# прерываются из-за настроек тайм-аута сеанса, что означает, что системы
# прерывают соединения после того, как видят, что для получения ответов
# на запросы требуется больше времени, чем некоторый максимально
# допустимый порог. DDoS-атака может сделать недоступным сайт, который человек
# планирует использовать. Например, 21 октября 2016 года многие
# пользователи не смогли получить доступ к нескольким известным сайтам,
# включая X (тогда известный как Twitter), PayPal, CNN, The Guardian, HBO
# Now и десяткам других популярных сайтов, из-за массированной DDoSатаки, предпринятой против третьей стороны, предоставляющей
# различные технические услуги для этих сайтов и многих других. Возможность DDoS-атак является одной из причин, по которой
# вам никогда не следует ждать до последней минуты, чтобы совершить
# онлайн-платеж или банковскую транзакцию со строгим сроком оплаты —
# нужный вам сайт может быть недоступен по ряду причин, включая
# продолжающуюся DDoS-атаку. DDoS-атака может привести к тому, что пользователи будут получать
# информацию с одного сайта, а не с другого. Делая один сайтнедоступным, пользователи Интернета, ищущие определенную
# информацию, вынуждены искать ее в другом месте и, следовательно, с
# большей вероятностью, чем до атаки, получить информацию с какого—
# либо другого сайта - явление, которое позволяет злоумышленникам либо
# распространять дезинформацию, либо не давать людям услышать
# определенную информацию или точки зрения по важным вопросам.
# Таким образом, DDoS-атаки могут быть использованы в качестве
# эффективного механизма — по крайней мере, в краткосрочной
# перспективе — для цензурирования противоположных точек зрения и
# продвижения пропаганды.

# ===================================================================================================================================================

import threading
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

# ---------- ТИПЫ МОТИВАЦИИ ДЛЯ АТАКИ ----------
class AttackMotive(Enum):
    FINANCIAL = "Финансовый ущерб (конкуренты, Чёрная пятница)"
    POLITICAL = "Политический (выборы, оппоненты)"
    HACKTIVISM = "Хактивизм (справедливость, протест)"
    CENSORSHIP = "Цензура и пропаганда"

# ---------- СИМУЛЯЦИЯ ЦЕЛЕВОГО САЙТА (жертвы) ----------
class Website:
    def __init__(self, name: str, capacity: int, is_critical: bool = False):
        self.name = name
        self.capacity = capacity          # макс. запросов в секунду
        self.request_log = []
        self.is_online = True
        self.is_critical = is_critical    # важный сайт (банк, платежи)
        self.lock = threading.Lock()
    
    def process_request(self, user_id: str) -> str:
        with self.lock:
            now = time.time()
            self.request_log.append((now, user_id))
            # оставляем запросы только за последнюю секунду
            self.request_log = [(t, u) for (t, u) in self.request_log if t > now - 1]
            
            if len(self.request_log) > self.capacity:
                self.is_online = False
                return f"❌ {self.name} НЕДОСТУПЕН (перегрузка)"
            
            return f"✅ {self.name} ответил пользователю {user_id}"
    
    def status(self) -> str:
        return "🟢 ДОСТУПЕН" if self.is_online else "🔴 НЕДОСТУПЕН"

# ---------- УСТРОЙСТВО-БОТ (компьютер, камера, роутер и т.д.) ----------
class BotDevice:
    def __init__(self, device_id: str, device_type: str, region: str):
        self.device_id = device_id
        self.device_type = device_type  # "Компьютер", "IP-камера", "Роутер", "Умный холодильник"
        self.region = region
        self.active = False
    
    def send_request(self, target: Website) -> str:
        # симуляция сетевой задержки
        time.sleep(random.uniform(0.005, 0.05))
        return target.process_request(f"{self.device_type}_{self.device_id}")
    
    def __repr__(self):
        return f"{self.device_type} [{self.region}] - {self.device_id}"

# ---------- БОТНЕТ (армия заражённых устройств) ----------
class Botnet:
    def __init__(self):
        self.bots: List[BotDevice] = []
        self.active_threads = []
        self.stop_event = threading.Event()
    
    def add_bot(self, bot: BotDevice):
        self.bots.append(bot)
    
    def add_realistic_bots(self, count: int):
        """Создаёт реалистичную смесь устройств из разных регионов"""
        device_types = ["Компьютер", "IP-камера", "Роутер", "Смарт-ТВ", "Умный холодильник", "NAS", "Принтер"]
        regions = ["США", "Европа", "Азия", "Россия", "Бразилия", "Индия", "Австралия"]
        
        for i in range(count):
            device_type = random.choice(device_types)
            region = random.choice(regions)
            bot = BotDevice(f"Bot_{i + 1}", device_type, region)
            self.bots.append(bot)
    
    def launch_attack(self, target: Website, duration_sec: int = 10):
        print(f"\n🔥 ЗАПУСК DDoS-АТАКИ на '{target.name}'")
        print(f"   Участвует устройств: {len(self.bots)}")
        print(f"   Мощность цели: {target.capacity} запросов/сек\n")
        
        def worker(bot: BotDevice):
            start_time = time.time()
            while not self.stop_event.is_set() and (time.time() - start_time) < duration_sec:
                bot.send_request(target)
        
        self.active_threads = []
        for bot in self.bots:
            t = threading.Thread(target = worker, args = (bot,))
            t.daemon = True
            t.start()
            self.active_threads.append(t)
    
    def stop_attack(self):
        self.stop_event.set()
        for t in self.active_threads:
            t.join(timeout=0.5)

# ---------- СИМУЛЯЦИЯ ПОЛЬЗОВАТЕЛЯ (влияние DDoS на людей) ----------
class InternetUser:
    def __init__(self, name: str):
        self.name = name
        self.failed_attempts = 0
    
    def try_access(self, website: Website, purpose: str):
        result = website.process_request(self.name)
        if "НЕДОСТУПЕН" in result:
            self.failed_attempts += 1
            print(f"🧑 {self.name} пытался {purpose} -> {result}")
        else:
            print(f"😊 {self.name}: {result}")
        return result

# ---------- СЦЕНАРИИ АТАК ИЗ ТЕКСТА ----------
class DDoSScenario:
    def __init__(self):
        self.botnet = Botnet()
    
    def scenario_financial_black_friday(self):
        """Финансовая мотивация: конкурент атакует интернет-магазин в Чёрную пятницу"""
        print("\n" + "=" * 70)
        print("💸 СЦЕНАРИЙ: ФИНАНСОВАЯ МОТИВАЦИЯ (Чёрная пятница)")
        print("Недобросовестный конкурент атакует онлайн-ритейлера в пик продаж")
        print("=" * 70)
        
        shop = Website("СуперМаркетОнлайн", capacity = 100)
        self.botnet.add_realistic_bots(80)  # 80 устройств (компьютеры + камеры + роутеры)
        
        # Пользователи пытаются купить товары
        users = [InternetUser(f"Покупатель_{i}") for i in range(20)]
        
        print("\n🛍️ ДО АТАКИ: пользователи делают покупки")
        for user in users[:5]:
            user.try_access(shop, "купить игрушку")
        
        input("\n⚡ НАЖМИТЕ ENTER, чтобы начать DDoS-атаку (конкурент нанимает ботнет)...")
        
        self.botnet.launch_attack(shop, duration_sec = 8)
        
        # Во время атаки пользователи не могут зайти
        print("\n😫 ВО ВРЕМЯ АТАКИ: сайт перегружен, покупатели теряют деньги")
        for _ in range(15):
            random.choice(users).try_access(shop, "оформить заказ со скидкой")
            time.sleep(0.2)
        
        self.botnet.stop_attack()
        time.sleep(1)
        
        print(f"\n📊 ИТОГ: {shop.name} - {shop.status()}")
        print("💰 УЩЕРБ: миллионы рублей потерянной выручки в выходные Чёрной пятницы")
    
    def scenario_political_election(self):
        """Политическая мотивация: атака на сайт оппонента во время выборов"""
        print("\n" + "=" * 70)
        print("🏛️ СЦЕНАРИЙ: ПОЛИТИЧЕСКАЯ МОТИВАЦИЯ")
        print("Коррумпированный политик отключает сайт конкурента в предвыборный сезон")
        print("=" * 70)
        
        opponent_site = Website("Кандидат_Иванов_За_Честные_Выборы", capacity = 60)
        self.botnet.add_realistic_bots(50)
        
        print(f"\n🗳️ Сайт оппонента: {opponent_site.status()}")
        
        input("\n👨‍💼 НАЖМИТЕ ENTER для запуска DDoS-атаки политиком...")
        
        self.botnet.launch_attack(opponent_site, duration_sec = 6)
        
        print("\n📰 Избиратели не могут получить программу кандидата")
        voter = InternetUser("Избиратель_Петров")
        voter.try_access(opponent_site, "читать предвыборную программу")
        
        self.botnet.stop_attack()
        
        print(f"\n📊 ИТОГ: Сайт оппонента - {opponent_site.status()}")
        print("🎭 ПОСЛЕДСТВИЕ: оппонент лишён возможности распространять свои сообщения")
    
    def scenario_hacktivism(self):
        """Хактивизм: атака на сайт полиции после инцидента"""
        print("\n" + "=" * 70)
        print("✊ СЦЕНАРИЙ: ХАКТИВИЗМ")
        print("Активисты атакуют сайт правоохранительных органов во имя 'справедливости'")
        print("=" * 70)
        
        police_site = Website("МВД_Регион", capacity = 80)
        self.botnet.add_realistic_bots(70)
        
        print(f"\n🚔 Сайт полиции: {police_site.status()}")
        print("💬 Хактивисты: 'Выключим их сайт в знак протеста!'")
        
        input("\n🌐 НАЖМИТЕ ENTER для запуска атаки...")
        
        self.botnet.launch_attack(police_site, duration_sec = 5)
        
        print("\n📢 Граждане не могут подать онлайн-заявление")
        citizen = InternetUser("Гражданин_Сидоров")
        citizen.try_access(police_site, "подать жалобу")
        
        self.botnet.stop_attack()
        print(f"\n⚖️ ИТОГ: {police_site.status()} - символическая победа активистов")
    
    def scenario_censorship_propaganda(self):
        """Цензура и пропаганда: один источник отключён, люди идут на другой"""
        print("\n" + "=" * 70)
        print("📺 СЦЕНАРИЙ: ЦЕНЗУРА И ПРОПАГАНДА")
        print("DDoS используется, чтобы заставить людей получать информацию с нужного сайта")
        print("=" * 70)
        
        independent_news = Website("Независимые_Новости", capacity = 50)
        propaganda_news = Website("Официальный_Вестник", capacity = 200)
        
        self.botnet.add_realistic_bots(60)
        
        print(f"\n📰 Независимые новости: {independent_news.status()}")
        print(f"📢 Официальный вестник: {propaganda_news.status()}")
        
        input("\n🎭 НАЖМИТЕ ENTER для атаки на независимые СМИ...")
        
        self.botnet.launch_attack(independent_news, duration_sec = 7)
        
        print("\n🧑‍💻 ПОЛЬЗОВАТЕЛИ ИЩУТ ИНФОРМАЦИЮ:")
        for i in range(10):
            user = InternetUser(f"Читатель_{i}")
            if random.random() < 0.3:
                user.try_access(independent_news, "читать новости")
            else:
                result = propaganda_news.process_request(user.name)
                print(f"📢 {user.name} зашёл на официальный сайт -> {result}")
            time.sleep(0.1)
        
        self.botnet.stop_attack()
        
        print(f"\n📊 ИТОГ: независимые СМИ - {independent_news.status()}")
        print("🔀 РЕЗУЛЬТАТ: люди вынуждены получать информацию с пропагандистского ресурса")
        print("⚠️ Это механизм цензурирования противоположных точек зрения")
    
    def scenario_impact_on_individuals(self):
        """Как DDoS влияет на обычных людей (из текста)"""
        print("\n" + "=" * 70)
        print("👤 ВЛИЯНИЕ DDoS НА ОБЫЧНЫХ ЛЮДЕЙ")
        print("=" * 70)
        
        # Ситуация 1: Оплата счета в последнюю минуту
        print("\n💳 ОПАСНОСТЬ: платеж в последнюю минуту")
        bank = Website("МойБанк", capacity = 30, is_critical = True)
        small_botnet = Botnet()
        small_botnet.add_realistic_bots(40)
        
        print("⚠️ Вы откладываете оплату кредита до 23:59")
        user = InternetUser("Клиент_банка")
        
        print("\n🔴 ВНЕЗАПНО: DDoS-атака на банк!")
        small_botnet.launch_attack(bank, duration_sec = 4)
        
        result = user.try_access(bank, "оплатить кредит до дедлайна")
        small_botnet.stop_attack()
        
        if "НЕДОСТУПЕН" in result:
            print("💸 ПОСЛЕДСТВИЕ: просрочка платежа, штраф, испорченная кредитная история")
        
        # Ситуация 2: Известный кейс 2016 года
        print("\n" + "-" * 50)
        print("🌍 ИСТОРИЧЕСКИЙ ПРИМЕР: 21 октября 2016 года")
        print("Атака на Dyn (DNS-провайдера) отключила:")
        compromised_sites = ["Twitter", "PayPal", "CNN", "The Guardian", "HBO Now", "Netflix", "Reddit"]
        print(", ".join(compromised_sites))
        print("🔧 Причина: DDoS на третью сторону, которая обслуживала эти сайты")
        print("👥 МИЛЛИОНЫ ПОЛЬЗОВАТЕЛЕЙ остались без доступа к любимым сервисам")

# ---------- ГЛАВНАЯ ДЕМОНСТРАЦИЯ ----------
def main():
    print("\n" + "=" * 70)
    print("🎯 СИМУЛЯЦИЯ DDoS-АТАК: АНАТОМИЯ, МОТИВЫ И ПОСЛЕДСТВИЯ")
    print("=" * 70)
    print("""
    По данным текста:
    • DDoS использует множество устройств (компьютеры, камеры, роутеры)
    • Мотивы: финансовые, политические, хактивизм, цензура
    • Влияние: потеря дохода, дезинформация, пропаганда, срыв платежей
    """)
    
    scenarios = DDoSScenario()
    
    # Запускаем все сценарии
    scenarios.scenario_financial_black_friday()
    input("\n👉 Нажмите Enter для следующего сценария...")
    
    scenarios.scenario_political_election()
    input("\n👉 Нажмите Enter для следующего сценария...")
    
    scenarios.scenario_hacktivism()
    input("\n👉 Нажмите Enter для следующего сценария...")
    
    scenarios.scenario_censorship_propaganda()
    input("\n👉 Нажмите Enter для следующего сценария...")
    
    scenarios.scenario_impact_on_individuals()
    
    print("\n" + "=" * 70)
    print("📌 ВЫВОДЫ ИЗ ТЕКСТА:")
    print("""
    1. DDoS-атаки — растущая угроза (услуги 'DDoS по найму' в тёмной сети)
    2. Могут быть финансовым оружием (конкуренты в Чёрную пятницу)
    3. Используются в политических целях (ограничение доступа оппонентов)
    4. Инструмент цензуры и распространения пропаганды
    5. Влияют на людей: срыв платежей, замедление интернета, дезинформация
    """)
    print("⚠️ ПРОГРАММА СОЗДАНА ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ")
    print("=" * 70)

if __name__ == "__main__":
    main()