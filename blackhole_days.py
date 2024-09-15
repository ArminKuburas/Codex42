import math

# XP Table (level: (xp to next level, total xp))
xp_table = {
    0: (0, 0),
    1: (462, 462),
    2: (2226, 2688),
    3: (3197, 5885),
    4: (5892, 11777),
    5: (17440, 29217),
    6: (17038, 46255),
    7: (17304, 63559),
    8: (10781, 74340),
    9: (11143, 85483),
    10: (9517, 95000),
    11: (10630, 105630),
    12: (18816, 124446),
}

def level_to_xp(level):
    level_base = int(level)
    progress = level - level_base  # decimal part of level

    if level_base in xp_table and (level_base + 1) in xp_table:
        current_total_xp = xp_table[level_base][1]
        next_level_xp = xp_table[level_base + 1][1]
        xp_to_next_level = xp_table[level_base + 1][0]

        interpolated_xp = current_total_xp + (progress * xp_to_next_level)
        return interpolated_xp
    else:
        return None  # Handle cases outside the table

def xp_to_level(xp):
    for level, (_, total_xp) in xp_table.items():
        if xp < total_xp:
            prev_level = level - 1
            prev_total_xp = xp_table[prev_level][1]
            xp_to_next = total_xp - prev_total_xp
            progress = (xp - prev_total_xp) / xp_to_next
            return prev_level + progress
    return max(xp_table.keys())  # If over max level, return highest

def calculate_days(current_xp, project_xp_gain):
    total_xp_before = current_xp
    total_xp_after = current_xp + project_xp_gain
    
    factor = 49980
    days_before = (total_xp_before / factor) ** 0.45
    days_after = (total_xp_after / factor) ** 0.45
    
    return (days_after - days_before) * 483

def display_art():
    print("\n")
print(r"""
 ____  _               _____ _  ___    _  ____  _      ______   _____      __     _______ 
 |  _ \| |        /\   / ____| |/ / |  | |/ __ \| |    |  ____| |  __ \   /\\ \   / / ____|
 | |_) | |       /  \ | |    | ' /| |__| | |  | | |    | |__    | |  | | /  \\ \_/ / (___  
 |  _ <| |      / /\ \| |    |  < |  __  | |  | | |    |  __|   | |  | |/ /\ \\   / \___ \ 
 | |_) | |____ / ____ \ |____| . \| |  | | |__| | |____| |____  | |__| / ____ \| |  ____) |
 |____/|______/_/    \_\_____|_|\_\_|  |_|\____/|______|______| |_____/_/    \_\_| |_____/
			  BLACKHOLE DAYS CALCULATOR
""")

def main():
    display_art()
    
    while True:
        current_level = input("Enter your current level (e.g., 4.62): ")
        if current_level.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            current_level = float(current_level)
        except ValueError:
            print("Invalid level input. Please try again.")
            continue

        project_xp = input("Enter the XP you will get from the project: ")
        if project_xp.lower() == "exit":
            print("Goodbye!")
            break

        try:
            project_xp = float(project_xp)
        except ValueError:
            print("Invalid XP input. Please try again.")
            continue

        current_xp = level_to_xp(current_level)
        if current_xp is None:
            print("Error: Invalid level input.")
            continue

        days = calculate_days(current_xp, project_xp)
        print(f"Completing this project will give you approximately {days:.2f} days.")

        new_xp = current_xp + project_xp
        new_level = xp_to_level(new_xp)
        print(f"Your new level will be approximately: {new_level:.2f}")

        choice = input("Do you want to calculate again? (Type 'EXIT' to quit else just press enter): ")
        if choice.lower() == "exit": # Basically we lower the choice so any version of exit can be used so I dont have to deal with typos like Exit or eXit or whatever
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
