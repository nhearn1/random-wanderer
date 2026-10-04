
# main.py (guild hall lock by level + pub trigger)
import sys
from character import Character
from exploration import Explorer
from inventory import Inventory
from shops import Town
from quests import QuestBoard
from story import Story

def print_header(title):
    print("\n" + "="*60);  print(title);  print("="*60)

def main():
    print_header("Random Wanderer — Guild Hall Unlock")
    name = input("Enter your hero's name: ").strip() or "Hero"
    player = Character(name=name)
    inventory = Inventory()
    explorer = Explorer(player, inventory)
    town = Town(player, inventory)
    quests = QuestBoard(player, inventory)
    story = Story(player, inventory, explorer)

    while True:
        print_header("Main Menu")
        print(f"(Role: {player.role}  Lvl: {player.level})")
        print("1) Explore further")
        print("2) Inventory")
        print("3) Stats")
        print("4) Return to Town")
        print("5) Quit")
        choice = input("> ").strip()

        if choice == "1":
            explorer.explore_loop()
        elif choice == "2":
            inventory.show(player);  input("\n[enter] to continue...")
        elif choice == "3":
            player.show_stats();     input("\n[enter] to continue...")
        elif choice == "4":
            town_loop(town, quests, explorer, story, player)
        elif choice == "5":
            print("Goodbye!");  sys.exit(0)
        else:
            print("Invalid choice.")

def town_loop(town, quests, explorer, story, player):
    while True:
        print_header("Home Town")
        print("1) Pub (Quests)")
        print("2) Weapon smith")
        print("3) Armor smith")
        print("4) Magic shop")
        print("5) Explore")
        # Guild Hall visibility and lock text
        if player.level >= 5 and player.main_story_unlocked:
            print("6) Guild Hall (Main Story)")
        else:
            lock_reason = []
            if player.level < 5: lock_reason.append("Lv 5")
            if not player.main_story_unlocked: lock_reason.append("Talk to Pub Owner")
            print(f"6) Guild Hall (Locked: {', '.join(lock_reason)})")
        print("7) Leave town (back to main)")
        choice = input("> ").strip()
        if choice == "1":
            quests.pub_menu()
        elif choice == "2":
            town.weapon_smith()
        elif choice == "3":
            town.armor_smith()
        elif choice == "4":
            town.magic_shop()
        elif choice == "5":
            explorer.choose_region(); explorer.explore_loop()
        elif choice == "6":
            if player.level >= 5 and player.main_story_unlocked:
                story.menu()
            else:
                print("The Guild Hall remains closed to you for now.")
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
