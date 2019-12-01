from functools import reduce

from aoc.challenge_base import ChallengeBase

class CombatGroup:
    """
    Combat group within an army
    """
    def __init__(self, side, desc, units, hp, attack, attack_type, initiative, weaknesses, immunities):
        """
        Constructor
        side: side that the group belongs to (0: immune system, 1: infection)
        desc: description / ID for the group (used in debug output)
        units: initial unit count
        hp: hit points per unit
        attack: attack strength
        attack_type: attack type
        initiative: initiative value
        weaknesses: set of attack types we receive double damage from
        immunities: set of attack types we receive no damage from
        """
        self.side = side
        self.desc = desc
        self.units = units
        self.hp = hp
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    def effective_power(self):
        """
        Return effective power of the group
        """
        return self.units * self.attack

class StalemateError(RuntimeError):
    """
    Exception to raise when no units are killed in a combat round
    """
    pass

class Challenge(ChallengeBase):
    """
    Day 24 challenges
    """
    def set_up_test_armies(self):
        """
        Set up the example armies, for testing
        """
        self.groups = [
            # Immune system groups
            CombatGroup(0, 1, 17, 5390, 4507, "fire", 2, {"radiation", "bludgeoning"}, set()),
            CombatGroup(0, 2, 989, 1274, 25, "slashing", 3, {"bludgeoning", "slashing"}, {"fire"}),

            # Infection groups
            CombatGroup(1, 1, 801, 4706, 116, "bludgeoning", 1, {"radiation"}, set()),
            CombatGroup(1, 2, 4485, 2961, 12, "slashing", 4, {"fire", "cold"}, {"radiation"})
        ]

    def set_up_armies(self):
        """
        Hard-coded from input, no need to parse all this text
        """
        self.groups = [
            # Immune system groups
            CombatGroup(0, 1, 2743, 4149, 13, "radiation", 14, set(), set()),
            CombatGroup(0, 2, 8829, 7036, 7, "fire", 15, set(), set()),
            CombatGroup(0, 3, 1928, 10700, 50, "slashing", 3, {"cold"}, {"fire", "radiation", "slashing"}),
            CombatGroup(0, 4, 6051, 11416, 15, "bludgeoning", 20, set(), set()),
            CombatGroup(0, 5, 895, 10235, 92, "bludgeoning", 10, {"bludgeoning"}, {"slashing"}),
            CombatGroup(0, 6, 333, 1350, 36, "radiation", 12, set(), set()),
            CombatGroup(0, 7, 2138, 8834, 35, "cold", 11, {"bludgeoning"}, set()),
            CombatGroup(0, 8, 4325, 1648, 3, "bludgeoning", 8, {"cold", "fire"}, set()),
            CombatGroup(0, 9, 37, 4133, 1055, "radiation", 1, set(), {"radiation", "slashing"}),
            CombatGroup(0, 10, 106, 3258, 299, "cold", 13, set(), {"slashing", "radiation"}),

            # Infection groups
            CombatGroup(1, 1, 262, 8499, 45, "cold", 6, {"cold"}, set()),
            CombatGroup(1, 2, 732, 47014, 127, "bludgeoning", 17, {"cold", "bludgeoning"}, set()),
            CombatGroup(1, 3, 4765, 64575, 20, "radiation", 18, set(), set()),
            CombatGroup(1, 4, 3621, 19547, 9, "cold", 5, set(), {"radiation", "cold"}),
            CombatGroup(1, 5, 5913, 42564, 14, "slashing", 9, set(), {"radiation", "bludgeoning", "fire"}),
            CombatGroup(1, 6, 7301, 51320, 11, "fire", 2, {"radiation", "fire"}, {"bludgeoning"}),
            CombatGroup(1, 7, 3094, 23713, 14, "radiation", 19, {"slashing", "fire"}, set()),
            CombatGroup(1, 8, 412, 36593, 177, "slashing", 16, {"radiation", "bludgeoning"}, set()),
            CombatGroup(1, 9, 477, 35404, 146, "cold", 7, set(), set()),
            CombatGroup(1, 10, 332, 11780, 70, "slashing", 4, {"fire"}, set())
        ]

    def get_enemy_groups(self, group):
        """
        Return list of all groups that are enemies of the given group
        """
        return [g for g in self.groups if g.side != group.side]

    def compute_potential_damage(self, attacker, defender):
        """
        Compute how much damage the attacker would deal to defender (assuming defender has enough HP)
        """
        if attacker.attack_type in defender.immunities:
            return 0

        return attacker.effective_power() * (2 if attacker.attack_type in defender.weaknesses else 1)

    def run_combat_round(self):
        """
        Run a single round of combat
        """
        # Target selection phase
        targets = {}
        for attacker in sorted(self.groups, key=lambda g: (g.effective_power(), g.initiative), reverse=True):
            # This group should work out how much damage it will deal to each enemy group
            priorities = [(self.compute_potential_damage(attacker, d), d.effective_power(), d.initiative, d)
                          for d in self.get_enemy_groups(attacker) if d not in targets.values()]
            
            if priorities:
                top_priority = max(priorities)

                # We only attack if we could deal damage
                if top_priority[0] > 0:
                    targets[attacker] = top_priority[-1]

        # Attacking phase. For challenge pt 2, we need to check if anything was killed, too!
        killed_something = False
        for attacker in sorted(self.groups, key=lambda g: g.initiative, reverse=True):
            # Check it selected a target and isn't dead yet
            if attacker in targets.keys() and attacker.units >= 0:
                defender = targets[attacker]
                damage_to_deal = self.compute_potential_damage(attacker, defender)
                units_to_kill = damage_to_deal // defender.hp
                if units_to_kill:
                    killed_something = True
                    defender.units -= units_to_kill
        
        if not killed_something:
            raise StalemateError()

        # Bring out yer dead!
        self.groups = list(filter(lambda g: g.units >= 0, self.groups))

    def challenge1(self):
        """
        Day 24 challenge 1
        """
        self.set_up_armies()

        # Run combat rounds until no groups from one side remain
        while len({g.side for g in self.groups}) > 1:
            self.run_combat_round()

        print(f"Remaining units in winning army: {reduce(lambda x, cg: x + cg.units, self.groups, 0)}")

    def challenge2(self):
        """
        Day 24 challenge 2
        """
        # Try different boost levels...
        for boost in range(1000):
            self.set_up_armies()

            # Boost the immune system groups
            for g in self.groups:
                if g.side == 0:
                    g.attack += boost

            # Run combat
            try:
                while len({g.side for g in self.groups}) > 1:
                    self.run_combat_round()
            except StalemateError:
                print(f"Boost {boost}: stalemate.")
                continue

            # Did the immune system win?
            if 0 in {g.side for g in self.groups}:
                print(f"Boost {boost}: Reindeer won! {reduce(lambda x, cg: x + cg.units, self.groups, 0)} units left.")
                break
            else:
                print(f"Boost {boost}: Infection won :-(")