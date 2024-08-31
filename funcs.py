# Time Converter
def timeConvert(time):
    days = time // 86400
    hours = (time % 86400) // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60

    return [int(days), int(hours), int(minutes), seconds]

def recourcesGathered(player, allAchievements):
        # Gets the player's total gold farmed
        achievement_name = "Gold Grab"
        achievements = allAchievements
        # Sorts all the acheivements for Gold Grab
        achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
        # sets the acheivement to the value (gold farmed)
        achievements = achievements.value
        # Stores the current gold farmed to a variable
        goldGathered=achievements

        # Gets the player's total elixer farmed
        achievement_name = "Elixir Escapade"
        achievements = allAchievements
        # Sorts all the acheivements for Elixir Escapade
        achievements = next((ach for ach in achievements if ach.name == achievement_name), None)
        # sets the acheivement to the value (elixir farmed)
        achievements = achievements.value
        # Stores the current elixer farmed to a variable
        elixerGathered=achievements

        print(f'TEST:  Gold: {goldGathered} | Elixer: {elixerGathered}')

        return [int(goldGathered), int(elixerGathered)]