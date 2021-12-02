class Unit:
    def __init__(self, name="skeleton", attack=0, deffence=0, speed=5, damage=1, max_health=10,
                 flying=False, range_attack=False, quantity=1):
        self.name = name

        self.attack = attack
        self.deffence = deffence
        self.speed = speed
        self.damage = damage
        self.max_health = max_health

        self.current_health = max_health
        self.quantity = quantity

        self.flying = flying
        self.range_attack = range_attack

