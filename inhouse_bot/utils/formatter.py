import datetime

all_roles = ["Top", "Jungle", "Mid", "ADC", "Support", "Fill"]
secondary_roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
all_roles_lowercase = ["top", "jungle", "mid", "adc", "support", "fill"]
secondary_roles_lowercase = ["top", "jungle", "mid", "adc", "support"]

sql_role_map = {
    "top": "Top",
    "jungle": "Jungle",
    "mid": "Mid",
    "adc": "ADC",
    "support": "Support",
    "": None
}

def ping_user_by_id(id, ign):
    # return "<@!" + str(id) + ">"
    if id == 0:
        return ign
    else:
        return ping_id(id)


def can_fill(elo):
    if elo > 1500:
        return "Yes!"
    else:
        return "Not yet."


def format_time():
    x = datetime.datetime.now()
    return x.strftime("%H:%M EST, %b %d %Y")


def ping_id(id):
    return "<@!" + str(id) + ">"
