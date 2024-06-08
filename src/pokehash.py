from pokemon_formats import PokePaste
import pokebase as pb
import re
import random
import json
import base64

global gManual


### Checks the validity of the pokepaste link and returns the structure of the team if successful
def getTeamFromPokepaste(link):
    pattern = re.compile("https:\/\/pokepast\.es\/[a-fA-F0-9]+")
    if pattern.match(link):
        return PokePaste.retrieve_pokepaste(link)
    return ["False"]

### Gets the value to multiply stats by for natures
def natureRatio(nature, stat):
    data = {"Adamant":{"Increases":"Attack","Decreases":"Sp. Atk"},"Bashful":{"Increases":"Sp. Atk","Decreases":"Sp. Atk"},"Bold":{"Increases":"Defense","Decreases":"Attack"},"Brave":{"Increases":"Attack","Decreases":"Speed"},"Calm":{"Increases":"Sp. Def","Decreases":"Attack"},"Careful":{"Increases":"Sp. Def","Decreases":"Sp. Atk"},"Docile":{"Increases":"Defense","Decreases":"Defense"},"Gentle":{"Increases":"Sp. Def","Decreases":"Defense"},"Hardy":{"Increases":"Attack","Decreases":"Attack"},"Hasty":{"Increases":"Speed","Decreases":"Defense"},"Impish":{"Increases":"Defense","Decreases":"Sp. Atk"},"Jolly":{"Increases":"Speed","Decreases":"Sp. Atk"},"Lax":{"Increases":"Defense","Decreases":"Sp. Def"},"Lonely":{"Increases":"Attack","Decreases":"Defense"},"Mild":{"Increases":"Sp. Atk","Decreases":"Defense"},"Modest":{"Increases":"Sp. Atk","Decreases":"Attack"},"Naive":{"Increases":"Speed","Decreases":"Sp. Def"},"Naughty":{"Increases":"Attack","Decreases":"Sp. Def"},"Quiet":{"Increases":"Sp. Atk","Decreases":"Speed"},"Quirky":{"Increases":"Sp. Def","Decreases":"Sp. Def"},"Rash":{"Increases":"Sp. Atk","Decreases":"Sp. Def"},"Relaxed":{"Increases":"Defense","Decreases":"Speed"},"Sassy":{"Increases":"Sp. Def","Decreases":"Speed"},"Serious":{"Increases":"Speed","Decreases":"Speed"},"Timid":{"Increases":"Speed","Decreases":"Attack"}}
    if data[nature]["Increases"] == stat:
        #print("A Nature of " + nature + " gives a bonus of 1.1 to " + stat)
        return 1.1
    elif data[nature]["Decreases"] == stat:
        #print("A Nature of " + nature + " gives a penalty of 0.9 to " + stat)
        return 0.9
    else:
        #print("A Nature of " + nature + " gives no bonus to " + stat)
        return 1

### Gets the value to multiply damage by for attack/defense types
def typeRatio(attackType, defendTypes):
    data = {"Normal":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":2,"Poison":1,"Ground":1,"Flying":1,"Psychic":1,"Bug":1,"Rock":0.5,"Ghost":0,"Dragon":1,"Dark":1,"Steel":0.5,"Fairy":1},"Fire":{"Normal":1,"Fire":0.5,"Water":2,"Electric":1,"Grass":0.5,"Ice":0.5,"Fighting":1,"Poison":1,"Ground":2,"Flying":1,"Psychic":1,"Bug":0.5,"Rock":2,"Ghost":1,"Dragon":1,"Dark":1,"Steel":0.5,"Fairy":0.5},"Water":{"Normal":1,"Fire":0.5,"Water":0.5,"Electric":2,"Grass":2,"Ice":0.5,"Fighting":1,"Poison":1,"Ground":1,"Flying":1,"Psychic":1,"Bug":1,"Rock":2,"Ghost":1,"Dragon":1,"Dark":1,"Steel":0.5,"Fairy":1},"Electric":{"Normal":1,"Fire":1,"Water":1,"Electric":0.5,"Grass":1,"Ice":1,"Fighting":1,"Poison":1,"Ground":2,"Flying":0.5,"Psychic":1,"Bug":1,"Rock":1,"Ghost":1,"Dragon":1,"Dark":1,"Steel":0.5,"Fairy":1},"Grass":{"Normal":1,"Fire":2,"Water":0.5,"Electric":0.5,"Grass":0.5,"Ice":2,"Fighting":1,"Poison":2,"Ground":0.5,"Flying":2,"Psychic":1,"Bug":2,"Rock":1,"Ghost":1,"Dragon":1,"Dark":1,"Steel":1,"Fairy":1},"Ice":{"Normal":1,"Fire":2,"Water":1,"Electric":1,"Grass":1,"Ice":0.5,"Fighting":2,"Poison":1,"Ground":1,"Flying":2,"Psychic":1,"Bug":1,"Rock":2,"Ghost":1,"Dragon":1,"Dark":1,"Steel":2,"Fairy":1},"Fighting":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":1,"Poison":1,"Ground":1,"Flying":2,"Psychic":2,"Bug":0.5,"Rock":0.5,"Ghost":1,"Dragon":1,"Dark":0.5,"Steel":1,"Fairy":2},"Poison":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":0.5,"Ice":1,"Fighting":0.5,"Poison":0.5,"Ground":2,"Flying":1,"Psychic":2,"Bug":0.5,"Rock":1,"Ghost":1,"Dragon":1,"Dark":1,"Steel":1,"Fairy":0.5},"Ground":{"Normal":1,"Fire":1,"Water":2,"Electric":0,"Grass":2,"Ice":2,"Fighting":1,"Poison":0.5,"Ground":1,"Flying":1,"Psychic":1,"Bug":1,"Rock":0.5,"Ghost":1,"Dragon":1,"Dark":1,"Steel":1,"Fairy":1},"Flying":{"Normal":1,"Fire":1,"Water":1,"Electric":2,"Grass":0.5,"Ice":2,"Fighting":0.5,"Poison":1,"Ground":0,"Flying":1,"Psychic":1,"Bug":0.5,"Rock":2,"Ghost":1,"Dragon":1,"Dark":1,"Steel":1,"Fairy":1},"Psychic":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":0.5,"Poison":1,"Ground":1,"Flying":1,"Psychic":0.5,"Bug":2,"Rock":1,"Ghost":2,"Dragon":1,"Dark":2,"Steel":1,"Fairy":1},"Bug":{"Normal":1,"Fire":2,"Water":1,"Electric":1,"Grass":0.5,"Ice":1,"Fighting":0.5,"Poison":1,"Ground":0.5,"Flying":2,"Psychic":1,"Bug":1,"Rock":2,"Ghost":1,"Dragon":1,"Dark":1,"Steel":1,"Fairy":1},"Rock":{"Normal":0.5,"Fire":0.5,"Water":2,"Electric":1,"Grass":2,"Ice":1,"Fighting":2,"Poison":0.5,"Ground":2,"Flying":0.5,"Psychic":1,"Bug":1,"Rock":1,"Ghost":1,"Dragon":1,"Dark":1,"Steel":2,"Fairy":1},"Ghost":{"Normal":0,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":0,"Poison":0.5,"Ground":1,"Flying":1,"Psychic":1,"Bug":0.5,"Rock":1,"Ghost":2,"Dragon":1,"Dark":2,"Steel":1,"Fairy":1},"Dragon":{"Normal":1,"Fire":0.5,"Water":0.5,"Electric":0.5,"Grass":0.5,"Ice":2,"Fighting":1,"Poison":1,"Ground":1,"Flying":1,"Psychic":1,"Bug":1,"Rock":1,"Ghost":1,"Dragon":2,"Dark":1,"Steel":1,"Fairy":2},"Dark":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":2,"Poison":1,"Ground":1,"Flying":1,"Psychic":0,"Bug":2,"Rock":1,"Ghost":0.5,"Dragon":1,"Dark":0.5,"Steel":1,"Fairy":2},"Steel":{"Normal":0.5,"Fire":2,"Water":1,"Electric":1,"Grass":0.5,"Ice":0.5,"Fighting":2,"Poison":0,"Ground":2,"Flying":0.5,"Psychic":0.5,"Bug":0.5,"Rock":0.5,"Ghost":1,"Dragon":0.5,"Dark":1,"Steel":0.5,"Fairy":0.5},"Fairy":{"Normal":1,"Fire":1,"Water":1,"Electric":1,"Grass":1,"Ice":1,"Fighting":0.5,"Poison":2,"Ground":1,"Flying":1,"Psychic":1,"Bug":0.5,"Rock":1,"Ghost":1,"Dragon":0,"Dark":0.5,"Steel":2,"Fairy":1}}
    if len(defendTypes) == 1:
        value = data[defendTypes[0].type.name.title()][attackType.name.title()]
        if gManual == True:
            print("Attack of type " + attackType.name + " does " + str(value) + "x damage to type of " + defendTypes[0].type.name.title())
    else:
        value = data[defendTypes[0].type.name.title()][attackType.name.title()] * data[defendTypes[1].type.name.title()][attackType.name.title()]
        if gManual == True:
            print("Attack of type " + attackType.name + " does " + str(value)+ "x damage to type of " + defendTypes[0].type.name.title() + " / " + defendTypes[1].type.name.title())
    return value

### Gets the value to multiply damage by for STAB
def stabValue(moveType, monType):
    if len(monType) == 1:
        if moveType.name == monType[0].type.name:
            #print("Stab of mon type " + monType[0].type.name + " for move type " + moveType.name)
            return 1.5
    else:
        if moveType.name == monType[0].type.name or moveType.name == monType[1].type.name:
            #print("Stab of mon type " + monType[0].type.name + " / " + monType[1].type.name + " for move type " + moveType.name)
            return 1.5
    return 1

### Turns a human readable name into the API format
def normalizeName(name):
    nameTemp = name.lower().replace(" ","-")
    if nameTemp[len(nameTemp)-1] == "-":
       return nameTemp[:-1]
    else:
        return nameTemp

### Calculates the damage from the selected pokemon and move
def calcDamage(attackMon, attackMove, defendMon):
    move = pb.move(normalizeName(attackMove))
    attackMonStats = pb.pokemon(normalizeName(attackMon['species']))
    defendMonStats = pb.pokemon(normalizeName(defendMon['species']))
    if gManual == True:
            print(attackMon['species'] + " attacked " + defendMon['species'] + " using " + attackMove)
    if move.damage_class.name == "physical":
        attackStat = int((((attackMon['ivs']['Atk']+ 2 * attackMonStats.stats[1].base_stat + (attackMon['evs']['Atk']/4)) * attackMon['Level']/100) + 5) * natureRatio(attackMon['nature'],"Attack"))
        defendStat = int((((attackMon['ivs']['Def']+ 2 * attackMonStats.stats[2].base_stat + (attackMon['evs']['Def']/4)) * attackMon['Level']/100) + 5) * natureRatio(defendMon['nature'],"Defense"))
        #print("The physical attacking stat is: " + str(attackStat))
        #print("The physical defending stat is: " + str(defendStat))
    elif move.damage_class.name == "special":
        #print("special")
        attackStat = int((((attackMon['ivs']['SpA']+ 2 * attackMonStats.stats[3].base_stat + (attackMon['evs']['SpA']/4)) * attackMon['Level']/100) + 5) * natureRatio(attackMon['nature'],"Sp. Atk"))
        defendStat = int((((attackMon['ivs']['SpD']+ 2 * attackMonStats.stats[4].base_stat + (attackMon['evs']['SpD']/4)) * attackMon['Level']/100) + 5) * natureRatio(defendMon['nature'],"Sp. Def"))
        #print("The special attacking stat is: " + str(attackStat))
        #print("The special defending stat is: " + str(defendStat))
    elif move.damage_class.name == "status":
        if normalizeName(attackMove) == "protect":
            attackMon['Status'].append("protect")
        attackStat = 0
    else:
        print(move.damage_class.name)

    if "protect" in defendMon['Status']:
        attackStat = 0
        defendMon['Status'].remove("protect")
        
    if attackStat != 0:
        baseDamage = int(((((((attackMon['Level'] *2)/ 5) +2 ) * move.power * attackStat / defendStat)/50) + 2) * typeRatio(move.type,defendMonStats.types) * stabValue(move.type,attackMonStats.types))
    else:
        baseDamage = 0
    return baseDamage

### Converts the teams into a serial value
def serializeTeams(teamA, teamB):
    data = []
    for mon in teamA:
        newMon = {}
        newMon['species'] = mon['species']
        newMon['HP'] = mon['HP']
        newMon['Status'] = mon['Status']
        data.append(newMon)
    for mon in teamB:
        newMon = {}
        newMon['species'] = mon['species']
        newMon['HP'] = mon['HP']
        newMon['Status'] = mon['Status']
        data.append(newMon)
    serial = json.dumps(data)
    return serial

### Prints a pokemon's moves
def printMoves(mon):
    for i,move in enumerate(mon['moves']):
        print(str(i) + " - " + mon['moves'][i])

### Key generation process
def generateKey():
    privateKey = []
    ### Get Teams
    link = input("Please paste your first pokepaste link: \n")
    teamA = getTeamFromPokepaste(link)
    if teamA[0] == "False":
       input("Invalid link, try again: \n")
       teamA = getTeamFromPokepaste(link)
    privateKey.append(link)
    
    link = input("Please paste your second pokepaste link: \n")
    teamB = getTeamFromPokepaste(link)
    if teamB[0] == "False":
       input("Invalid link, try again: \n")
       teamB = getTeamFromPokepaste(link)
    privateKey.append(link)


    ### Setup Game
    for mon in teamA:
        monStats = pb.pokemon(normalizeName(mon['species']))
        mon["HP"] = int((mon['ivs']['HP']+ 2 * monStats.stats[0].base_stat + (mon['evs']['HP']/4)) * mon['Level']/100) + 10 + mon['Level']
        #print(mon['species'] + "のHP: " + str(mon['HP']))
        mon["Status"] = []

    for mon in teamB:
        monStats = pb.pokemon(normalizeName(mon['species']))
        mon["HP"] = int((mon['ivs']['HP']+ 2 * monStats.stats[0].base_stat + (mon['evs']['HP']/4)) * mon['Level']/100) + 10 + mon['Level']
        mon["Status"] = []

    ### Run Simulation
    currentMonA = random.randint(0,5)
    currentMonB = random.randint(0,5)
    counter = 1
    if gManual == True:
            for i,mon in enumerate(teamA):
                print(str(i) + " - " + mon['species'])
            currentMonA = -1
            while currentMonA < 0 or currentMonA > 5:
                currentMonA = int(input("Please select a Pokemon for Team A: "))
            for i,mon in enumerate(teamB):
                print(str(i) + " - " + mon['species'])
            currentMonB = -1
            while currentMonB < 0 or currentMonB > 5:
                currentMonB = int(input("Please select a Pokemon for Team B: "))
                
            print(teamA[currentMonA]['species'] + "のHP: " + str(teamA[currentMonA]['HP']))
            print(teamB[currentMonB]['species'] + "のHP: " + str(teamB[currentMonB]['HP']))
    privateKey.append((currentMonA,currentMonB))
    while teamA[currentMonA]['HP'] >= 0 and teamB[currentMonB]['HP'] >= 0:
        if counter%2 == 1:
            if gManual == True:
                moveIndex = -1
                while moveIndex > 3 or moveIndex < 0:
                    printMoves(teamA[currentMonA])
                    moveIndex = int(input("Please pick a move: \n"))
            else:
                moveIndex = random.randint(0,3)
            privateKey.append((currentMonA,moveIndex))
            damage = calcDamage(teamA[currentMonA],teamA[currentMonA]['moves'][moveIndex],teamB[currentMonB])
            teamB[currentMonB]['HP'] -= damage
            if gManual == True:
                print("The attack did " + str(damage) + " points of damage!  " + teamB[currentMonB]['species'] + " has only " + str(teamB[currentMonB]['HP']) + "HP remaining!")
        else:
            if gManual == True:
                moveIndex = -1
                while moveIndex > 3 or moveIndex < 0:
                    printMoves(teamB[currentMonB])
                    moveIndex = int(input("Please pick a move: \n"))
            else:
                moveIndex = random.randint(0,3)
            privateKey.append((currentMonB,moveIndex))
            damage = calcDamage(teamB[currentMonB],teamB[currentMonB]['moves'][moveIndex],teamA[currentMonA])
            teamA[currentMonA]['HP'] -= damage
            if gManual == True:
                print("The attack did " + str(damage) + " points of damage!  " + teamA[currentMonA]['species'] + " has only " + str(teamA[currentMonA]['HP']) + "HP remaining!")
        counter += 1



    ### Determine Hash
    print("Public Key: ")
    serial = serializeTeams(teamA,teamB)
    print(base64.b64encode(serial.encode('utf-8')).decode())

    print("Private Key: ")
    jsonData = json.dumps(privateKey)
    print(base64.b64encode(jsonData.encode('utf-8')).decode())



### Key check process
def checkKey():
    ### Parse the data
    privateKeyRaw = input("Private Key: \n")
    publicKeyRaw = input("Public Key: \n")
    decoded = base64.b64decode(privateKeyRaw)
    privateKey = json.loads(decoded)
    teamAUrl = privateKey[0]
    teamBUrl = privateKey[1]
    currentMonA = privateKey[2][0]
    currentMonB = privateKey[2][1]
    moves = privateKey[3:]

    ### Load and setup
    teamA = getTeamFromPokepaste(teamAUrl)
    teamB = getTeamFromPokepaste(teamBUrl)

    for mon in teamA:
        monStats = pb.pokemon(normalizeName(mon['species']))
        mon["HP"] = int((mon['ivs']['HP']+ 2 * monStats.stats[0].base_stat + (mon['evs']['HP']/4)) * mon['Level']/100) + 10 + mon['Level']
        mon["Status"] = []

    for mon in teamB:
        monStats = pb.pokemon(normalizeName(mon['species']))
        mon["HP"] = int((mon['ivs']['HP']+ 2 * monStats.stats[0].base_stat + (mon['evs']['HP']/4)) * mon['Level']/100) + 10 + mon['Level']
        mon["Status"] = []

    ### Simulate battle based on private key
    counter = 1
    for move in moves:
        if counter%2 == 1:
            moveIndex = move[1]
            damage = calcDamage(teamA[currentMonA],teamA[currentMonA]['moves'][moveIndex],teamB[currentMonB])
            teamB[currentMonB]['HP'] -= damage
            #print("The attack did " + str(damage) + " points of damage!  " + teamB[currentMonB]['species'] + " has only " + str(teamB[currentMonB]['HP']) + "HP remaining!")
        else:
            moveIndex = move[1]
            damage = calcDamage(teamB[currentMonB],teamB[currentMonB]['moves'][moveIndex],teamA[currentMonA])
            teamA[currentMonA]['HP'] -= damage
            #print("The attack did " + str(damage) + " points of damage!  " + teamA[currentMonA]['species'] + " has only " + str(teamA[currentMonA]['HP']) + "HP remaining!")
        counter += 1

    ### Generate and check output against public key
    serialPubKey = serializeTeams(teamA,teamB)
    checkPubKey = base64.b64encode(serialPubKey.encode('utf-8'))
    if checkPubKey.decode() == publicKeyRaw:
        print("Authorized")
    else:
        print("Unauthorized")


### Main loop
if __name__ == "__main__":
    while True:
        choice = input("1 - Generate Keypair (Automatic)\n2 - Generate Keypair (Manual)\n3 - Check Key\n>")
        if choice == "1":
            gManual = False
            generateKey()
        if choice == "2":
            gManual = True
            generateKey()
        elif choice == "3":
            checkKey()
        else:
            pass
        


