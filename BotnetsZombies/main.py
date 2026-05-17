# Ботнеты и зомби
# Часто в DDoS-атаках используются так называемые ботнеты. Ботнеты - это
# совокупность скомпрометированных компьютеров, которые принадлежат
# другим сторонам, но которыми хакер удаленно управляет и использует для
# выполнения задач без ведома законных владельцев.
# Преступники, которые успешно заражают вредоносным ПО несколько
# миллионов компьютеров, могут, например, потенциально использовать эти
# машины, известные как зомби, для одновременной отправки множества
# запросов с одного сервера или серверной фермы в попытке перегрузить цель трафиком.

# ===================================================================================================================================================

import threading
import time
import random
from dataclasses import dataclass
from typing import List, Dict
import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BotnetSimulator")

@dataclass
class Bot:
    """Модель одного зараженного компьютера (зомби)"""
    bot_id: int
    ip_address: str
    is_active: bool = True
    
    def send_request(self, target_url: str) -> None:
        """Симуляция отправки HTTP-запроса (без реальной отправки)"""
        if not self.is_active:
            return
        # Эмуляция сетевой задержки
        delay = random.uniform(0.01, 0.05)
        time.sleep(delay)
        logger.debug(f"Бот {self.bot_id} ({self.ip_address}) отправляет запрос на {target_url}")

class Botnet:
    """Симулятор ботнета - НЕ для реального использования"""
    
    def __init__(self, name: str, c2_server: str = "simulated-c2.local"):
        self.name = name
        self.c2_server = c2_server
        self.bots: List[Bot] = []
        self.is_attacking = False
        self.attack_thread = None
    
    def add_bot(self, bot: Bot) -> None:
        """Добавить скомпрометированный компьютер"""
        self.bots.append(bot)
        logger.info(f"Бот {bot.bot_id} добавлен в ботнет {self.name}. Всего ботов: {len(self.bots)}")
    
    def remove_bot(self, bot_id: int) -> None:
        """Удалить бот (например, владелец вылечил компьютер)"""
        self.bots = [b for b in self.bots if b.bot_id != bot_id]
        logger.info(f"Бот {bot_id} удалён. Осталось: {len(self.bots)}")
    
    def command_all(self, command: str, target: str = None) -> None:
        """Разослать команду всем ботам"""
        logger.info(f"Команда C2: {command} для {len(self.bots)} ботов")
        
        if command == "attack" and target:
            self._start_attack(target)
        elif command == "sleep":
            self._stop_attack()
        elif command == "status":
            self._report_status()
    
    def _start_attack(self, target: str) -> None:
        """Симуляция DDoS-атаки - без реальных запросов вне симуляции"""
        if self.is_attacking:
            logger.warning("Атака уже идёт")
            return
        
        self.is_attacking = True
        logger.warning(f"⚠️ СИМУЛЯЦИЯ: ботнет {self.name} атакует {target}")
        
        def attack_loop():
            while self.is_attacking:
                # Каждый бот "отправляет запрос" с некоторой вероятностью
                active_bots = [b for b in self.bots if b.is_active]
                for bot in active_bots:
                    bot.send_request(target)
                time.sleep(0.1)  # Пауза, чтобы не загружать процессор
        
        self.attack_thread = threading.Thread(target = attack_loop, daemon = True)
        self.attack_thread.start()
    
    def _stop_attack(self) -> None:
        self.is_attacking = False
        logger.info("Атака остановлена")
    
    def _report_status(self) -> None:
        active = sum(1 for b in self.bots if b.is_active)
        logger.info(f"Ботнет {self.name}: всего {len(self.bots)} ботов, активно {active}")
    
    def simulate_infection(self, count: int) -> None:
        """Симуляция заражения новых машин"""
        logger.info(f"Заражение {count} новых компьютеров...")
        for i in range(count):
            new_id = len(self.bots) + 1
            fake_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
            self.add_bot(Bot(bot_id = new_id, ip_address = fake_ip))


# Пример использования (только в образовательных целях)
if __name__ == "__main__":
    print("=" * 60)
    print("ОБРАЗОВАТЕЛЬНАЯ СИМУЛЯЦИЯ ПРИНЦИПОВ РАБОТЫ БОТНЕТА")
    print("Никакие реальные атаки или заражения не производятся.")
    print("=" * 60)
    
    # Создаём ботнет под управлением C2
    botnet = Botnet(name = "DemoBotnet")
    
    # Симулируем заражение 5 компьютеров
    botnet.simulate_infection(5)
    
    # Проверяем статус
    botnet.command_all("status")
    
    # Симулируем DDoS-атаку на учебный хост (никто не атакуется реально)
    print("\n--- Симуляция атаки ---")
    botnet.command_all("attack", target = "example.com")
    
    # Даём атаке поработать 2 секунды
    time.sleep(2)
    
    # Останавливаем атаку
    botnet.command_all("sleep")
    
    # Удаляем один "вылеченный" компьютер
    botnet.remove_bot(bot_id = 3)
    
    # Финальный статус
    botnet.command_all("status")
    
    print("\n✅ Симуляция завершена. Помните: реальные ботнеты — это уголовное преступление.")