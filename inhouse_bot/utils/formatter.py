def ping_user_by_id(id, ign):
    if id == 0:
        return ign
    else:
        return ("<@!" + str(id) + "> ")
def can_fill(elo):
    if elo > 1500:
        return "Yes!"
    else:
        return "Not yet."