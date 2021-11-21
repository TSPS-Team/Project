class Unit:
    def __init__(self, attack=0, deffence=0, magic_resist=0, speed=5, damage=1, max_health=10, flying=False,
                 range_attack=False):
        self.attack = attack
        self.deffence = deffence
        self.magic_resist = magic_resist
        self.speed = speed

        self.damage = damage
        self.max_health = max_health
        self.current_health = max_health

        self.flying = flying
        self.range_attack = range_attack

