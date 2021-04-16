import os

name = input("Enter ship name: ").replace(" ", "_")

voicenames = {
    "profile" : "SelfIntro",
    "get" : "Intro",
    "login" : "Log",
    "detail" : "Details",
    "main" : "SecIdle",
    "touch_head" : "Headpat",
    "touch" : "Sec",
    "task" : "Task",
    "mission_complete" : "TaskC",
    "mail" : "Mail",
    "home" : "MissionFin",
    "expedition" : "Commission",
    "upgrade" : "Str",
    "warcry" : "MissionStart",
    "mvp" : "MVP",
    "lose" : "Defeat",
    "skill" : "SkillActivation",
    "hp" : "LowHP",
    "feeling" : "Affinity_",
    "propose" : "Pledge",
    "link" : "Extra_",
    "extra" : "TitleScreen"
}

multiples = ["SecIdle", "Sec", "Affinity", "Extra"]

path = "./input/"
original = [f for f in os.listdir(path) if os.path.isfile(path + f) and not "present" in f]
files = [*original]
for i in range(len(files)):
    files[i] = files[i].replace(".ogg", "")
    for k in voicenames.keys():
        files[i] = files[i].replace(k, voicenames[k])

for i in range(len(files)):
    f = files[i]
    file = name + "_"

    if "_" in f:
        split = f.split("_")
        line = skin = "0"

        if len(split) == 3:
            if split[0] in multiples:
                line = split[1]
                skin = split[2]

        elif len(split) == 2:
            if split[0] in multiples:
                line = split[1]
            else:
                skin = split[1]

        file += split[0]
        if line != "0":
            if split[0] == "Affinity":
                line = str(int(line) - 1)
            file += line
        if skin != "0":
            if skin == "ex1100":
                file += "BasePostPledge"
            else:
                file += "Skin" + skin
    else:
        file += f
    file += "JP.ogg"

    os.rename(path + original[i], path + file)

for f in os.listdir(path):
    if "present" in f or "profile" in f:
        os.remove(path + f)