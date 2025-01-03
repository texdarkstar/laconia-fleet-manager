
def get_model_id_by_name(fleetmanager, model_name):
    resp = fleetmanager.db.table("ship_models").select("*").eq("name", model_name).execute().data

    if resp:
        return resp[0]['id']


def get_model_name_by_id(fleetmanager, model_id):
    resp = fleetmanager.db.table("ship_models").select("*").eq("id", model_id).execute().data

    if resp:
        return resp[0]['name']


def get_shipyard_id_by_name(fleetmanager, shipyard):
    resp = fleetmanager.db.table("shipyards").select("*").eq("name", shipyard).execute().data

    if resp:
        return resp[0]['id']


def get_shipyard_name_by_id(fleetmanager, shipyard_id):
    resp = fleetmanager.db.table("shipyards").select("*").eq("id", shipyard_id).execute().data

    if resp:
        return resp[0]['name']


def get_hull_number(fleetmanager, ship_id: int):
    ship_list = fleetmanager.db.table("ships").select("*").execute().data

    models = {}
    same_models = []

    for row in fleetmanager.db.table("ship_models").select("*").execute().data:
        models[row["id"]] = row["classification"]

    ship = fleetmanager.db.table("ships").select("*").eq("id", ship_id).execute().data.pop()

    for row in ship_list:
        if row["model_id"] == ship["model_id"]:
            same_models.append(row["id"])

    n = same_models.index(ship["id"]) + 1
    zero = ""

    if int(n) < 10:
        zero = "0"

    hull_string = models[ship["model_id"]] + f"-{zero}" + str(n)


    return hull_string


def new_hull(fleetmanager, model_id):
    hull_classification = (
        fleetmanager.db.table("ship_models")
        .select("*").eq("id", model_id)
        .execute().data.pop()["classification"])


    ships = fleetmanager.db.table("ships").select("*").eq("model_id", model_id).execute().data

    n = str(len(ships) + 1)

    if int(n) < 10:
        n = "0" + n

    hull_classification += "-" + n

    return hull_classification


def get_ships_by_userid(fleetmanager, user_id):
    resp = fleetmanager.db.table("ships").select("*").eq("registered_to", user_id).execute()

    return resp.data


def get_ships_by_shipid(fleetmanager, ship_id):
    resp = fleetmanager.db.table("ships").select("*").eq("id", ship_id).execute()

    if resp.data:
        return resp.data.pop()
    else:
        return []


def is_officer(user):
    auth = False
    for role in user.roles:
        if role.name == "Officer":
            auth = True

    return auth


def is_fullmember(user):
    auth = False
    for role in user.roles:
        if role.name == "Member":
            auth = True

    return is_officer(user) or auth

