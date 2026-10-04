
# story.py
import random
from combat import fight
from enemy import Enemy
from data import MONSTERS

class Story:
    """
    Story stages (acts):
      0 = Prologue (not started)
      1 = Act I  : Corrupted Alpha Bear (Woods)
      2 = Act II : Pirate Warlord (Beach)
      3 = Act III: Undead Chieftain (Plains)
      4 = Act IV : Dark Mage General (Mountains)
      5 = Trial  : Trial Knight (Capital arena)
      6 = Pre-Finale: Corruption Avatar
      7 = Finale : Choice + Kaelen (optional duel)
      8 = Epilogue complete
    """
    def __init__(self, player, inventory, explorer):
        self.player = player
        self.inventory = inventory
        self.explorer = explorer

    def menu(self):
        while True:
            print("\n-- Guild Hall (Main Story) --")
            print(f"Story Stage: {self.player.story_stage}")
            st = self.player.story_stage
            if st == 0:
                self._scene("Pub Owner", "Stranger, the woods are restless... something massive prowls at dusk.")
                print("1) Begin Act I (Hunt the Corrupted Alpha Bear)")
                print("0) Leave")
                if input("> ").strip() == "1":
                    self.player.story_stage = 1
                else:
                    return
            elif st == 1:
                self._scene("Guild Scribe", "Target: Corrupted Alpha Bear, deep in the Woods.")
                if self._boss("corrupted alpha bear", 1.10, 1.05) == "won":
                    self._scene("Guild Scribe", "Impressive. Raiders mass at the Beach—stop their Warlord.")
                    self.player.story_stage = 2
                return
            elif st == 2:
                self._scene("Harbor Master", "Cut off the Warlord and the raiders scatter.")
                if self._boss("pirate warlord", 1.12, 1.05) == "won":
                    self._scene("High Knight", "Undead banners rise across the Plains. Break their Chieftain.")
                    self.player.story_stage = 3
                return
            elif st == 3:
                self._scene("Ranger", "Skulls drum in the grass. The Undead Chieftain commands from a cairn.")
                if self._boss("undead chieftain", 1.15, 1.08) == "won":
                    self._scene("High Knight", "A Dark Mage General gathers power in the Mountains. End him.")
                    self.player.story_stage = 4
                return
            elif st == 4:
                self._scene("Scout", "Thin air, black glass armor, cruel magic.")
                if self._boss("dark mage general", 1.18, 1.10) == "won":
                    self._scene("King's Herald", "To the Capital. Prove yourself in trial before the court.")
                    self.player.story_stage = 5
                return
            elif st == 5:
                self._scene("High Knight", "Steel answers only to steel. Face the Trial Knight in the arena.")
                if self._boss("trial knight", 1.20, 1.12, 1.10) == "won":
                    self._scene("Seer", "The corruption itself gathers form. Strike at its Avatar.")
                    self.player.story_stage = 6
                return
            elif st == 6:
                self._scene("Seer", "All threads knot here. Break the Avatar and choose your path.")
                if self._boss("corruption avatar", 1.25, 1.12, 1.10) == "won":
                    self._scene("Kaelen", "You've seen the rot in the crown. Choose.")
                    self.player.story_stage = 7
                return
            elif st == 7:
                print("\nFinale — choose your ending:")
                print("1) Accept the King's honor (Hero)")
                print("2) Side with Kaelen (Rebel)")
                print("3) Walk away (Wanderer)")
                print("4) Challenge Kaelen (optional duel)")
                print("0) Leave")
                c = input("> ").strip()
                if c == "1":
                    self._scene("King", "Kneel. Rise a hero of the realm.")
                    self._end("Hero");  return
                elif c == "2":
                    self._scene("Kaelen", "Then we break the old order together.")
                    self._end("Rebel"); return
                elif c == "3":
                    self._scene("Pub Owner", "Some legends slip quietly out the back door.")
                    self._end("Wanderer"); return
                elif c == "4":
                    if self._boss("kaelen", 1.22, 1.18, 1.12) == "won":
                        self._scene("Narrator", "You carve your own ending in steel and silence.")
                        self._end("Wanderer")
                    return
                else:
                    return
            else:
                print("Story complete. (Epilogue)")
                print("0) Leave")
                if input("> ").strip() == "0":
                    return

    def _scene(self, speaker, text):
        print(f"\n[{speaker}] {text}")

    def _scaled_enemy(self, name):
        m = MONSTERS[name]
        lvl = max(1, self.player.level)
        hp = int(m["hp"] + m.get("hp_per_level", 0) * (lvl - 1))
        atk = int(m["atk"] + m.get("atk_per_level", 0) * (lvl - 1))
        df  = int(m["def"] + m.get("def_per_level", 0) * (lvl - 1))
        return Enemy(name=name, hp=hp, atk=atk, defense=df, xp=m.get("xp", 30),
                     gold_range=m.get("gold", (10, 25)), drop=m.get("drop"))

    def _boss(self, name, bump_hp=1.0, bump_atk=1.0, bump_def=1.0):
        e = self._scaled_enemy(name)
        e.hp  = int(e.hp  * bump_hp)
        e.atk = int(e.atk * bump_atk)
        e.defense = int(e.defense * bump_def)
        outcome = fight(self.player, [e], inventory=self.inventory)
        if outcome == "won" and hasattr(e, "gold_range"):
            import random
            self.player.gold += random.randint(*e.gold_range)
        return outcome

    def _end(self, ending_name):
        self.player.ending_unlocked = True
        self.player.story_stage = 8
        print(f"\n*** Ending unlocked: {ending_name} ***")
