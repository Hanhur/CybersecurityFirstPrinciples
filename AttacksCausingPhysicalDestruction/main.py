# Атаки, приводящие к физическому разрушению
# Поскольку столь значительная часть нашей жизни была преобразована в
# цифровую форму, то есть стала компьютеризированной, злоумышленники
# теперь могут легко использовать кибератаки для нанесения физического
# ущерба. Как отмечалось выше, саботаж заводских систем может привести к
# появлению на рынке дефектной (и, возможно, чрезвычайно опасной)
# продукции. Также нетрудно понять, как вмешательство в медицинские
# системы может привести к смерти людей или как нарушение работы
# холодильных систем в продовольственных магазинах может привести к
# распространению болезней. Возможны и косвенные разрушения —
# например, отключение пожарной сигнализации или системы 911 от сети
# может привести к тому, что пожары станут гораздо более разрушительными,
# чем они были бы в противном случае.

# ===================================================================================================================================================

"""
Моделирование кибератак, приводящих к физическому разрушению
На основе текста: саботаж заводских систем, вмешательство в медсистемы,
нарушение работы холодильных систем, отключение пожарной сигнализации/911.
"""

import random
import time
from enum import Enum

# --------------------------------------------
# 1. Саботаж заводских систем (дефектная продукция)
# --------------------------------------------
class FactorySystem:
    def __init__(self):
        self.quality_control_active = True
        self.production_speed = 1.0  # нормальная скорость
    
    def sabotage_quality_control(self):
        print("[ЗАВОД] Взлом системы контроля качества...")
        self.quality_control_active = False
        print("[ЗАВОД] Контроль качества ОТКЛЮЧЁН. Выпускается опасная продукция.")
    
    def produce_item(self):
        if not self.quality_control_active:
            defect = random.choice(["норма", "дефект", "критический дефект"])
            if defect == "критический дефект":
                print("   ⚠️ Произведено ИЗДЕЛИЕ С КРИТИЧЕСКИМ ДЕФЕКТОМ (может взорваться/сломаться)")
                return "dangerous"
            elif defect == "дефект":
                print("   ⚠️ Произведено изделие с дефектом")
                return "defective"
        print("   Произведено нормальное изделие")
        return "normal"

# --------------------------------------------
# 2. Вмешательство в медицинские системы
# --------------------------------------------
class MedicalSystem:
    def __init__(self):
        self.heart_monitor_active = True
        self.drug_infusion_active = True
        self.patient_state = "stable"
    
    def attack_medical_devices(self):
        print("\n[БОЛЬНИЦА] Кибератака на медицинские устройства...")
        self.heart_monitor_active = False
        self.drug_infusion_active = False
        print("[БОЛЬНИЦА] ❌ Мониторы отключены, системы ввода лекарств заблокированы!")
    
    def simulate_patient(self):
        if not self.heart_monitor_active:
            print("   🚨 Медсестра: пациент в критическом состоянии, но системы молчат!")
            self.patient_state = "critical"
            # имитация ухудшения
            if random.random() < 0.3:
                print("   💀 ЛЕТАЛЬНЫЙ ИСХОД из-за отсутствия мониторинга и инфузии.")
                return "death"
        return "alive"

# --------------------------------------------
# 3. Нарушение работы холодильных систем (продовольственный магазин)
# --------------------------------------------
class RefrigerationSystem:
    def __init__(self):
        self.temperature = 4.0  # нормальные градусы
        self.alarm_active = True
    
    def hack_refrigeration(self):
        print("\n[МАГАЗИН] Взлом холодильной системы...")
        self.alarm_active = False
        print("[МАГАЗИН] ❌ Сигнализация отключена, температура повышается.")
    
    def raise_temperature(self):
        if not self.alarm_active:
            self.temperature += random.uniform(0.5, 1.5)
            print(f"   Температура в холодильнике: {self.temperature:.1f}°C")
            if self.temperature > 8.0:
                print("   🦠 Рост бактерий! Продукты испорчены — риск вспышки болезней.")
                return "spoiled"
        return "ok"

# --------------------------------------------
# 4. Отключение пожарной сигнализации / 911
# --------------------------------------------
class EmergencySystem:
    def __init__(self):
        self.fire_alarm_active = True
        self.nine_one_one_active = True
    
    def disconnect_systems(self):
        print("\n[ЭКСТРЕННЫЕ СЛУЖБЫ] Кибератака на системы безопасности...")
        self.fire_alarm_active = False
        self.nine_one_one_active = False
        print("[ЭКСТРЕННЫЕ СЛУЖБЫ] ❌ Пожарная сигнализация и 911 ОТКЛЮЧЕНЫ!")
    
    def simulate_fire(self):
        if random.random() < 0.4:  # имитация возгорания
            print("   🔥 Начался пожар! Сигнализация молчит.")
            if not self.fire_alarm_active:
                print("   🚒 Пожарные не вызваны (911 не работает). Ущерб КАТАСТРОФИЧЕСКИЙ.")
                return "catastrophic_damage"
            else:
                print("   ✅ Пожарные приехали вовремя, ущерб минимален.")
        return "no_fire"

# --------------------------------------------
# Главная демонстрация всех атак
# --------------------------------------------
def main():
    print("=" * 60)
    print("МОДЕЛИРОВАНИЕ КИБЕРАТАК С ФИЗИЧЕСКИМ РАЗРУШЕНИЕМ")
    print("=" * 60)
    
    # Сценарий 1: завод
    factory = FactorySystem()
    print("\n--- СЦЕНАРИЙ 1: Саботаж завода ---")
    factory.sabotage_quality_control()
    for _ in range(5):
        factory.produce_item()
        time.sleep(0.3)
    
    # Сценарий 2: больница
    hospital = MedicalSystem()
    print("\n--- СЦЕНАРИЙ 2: Вмешательство в медсистемы ---")
    hospital.attack_medical_devices()
    hospital.simulate_patient()
    
    # Сценарий 3: продовольственный магазин
    store = RefrigerationSystem()
    print("\n--- СЦЕНАРИЙ 3: Нарушение холодильных систем ---")
    store.hack_refrigeration()
    for _ in range(4):
        result = store.raise_temperature()
        if result == "spoiled":
            print("   🦠 Эпидемиологический риск из-за испорченной еды!")
        time.sleep(0.5)
    
    # Сценарий 4: отключение экстренных служб
    emergency = EmergencySystem()
    print("\n--- СЦЕНАРИЙ 4: Отключение пожарной сигнализации и 911 ---")
    emergency.disconnect_systems()
    emergency.simulate_fire()
    
    print("\n" + "=" * 60)
    print("ВЫВОД: Кибератаки могут приводить к прямым и косвенным")
    print("физическим разрушениям, болезням и гибели людей.")
    print("=" * 60)

if __name__ == "__main__":
    main()