def get_model_name_by_id(fleetmanager, model_id):
    # resp = fleetmanager.db.table("ship_models").select("*").eq("id", model_id).execute().data
    for model in fleetmanager.cached_tables["ship_models"]:
        if int(model["id"]) == int(model_id):
            return model["name"]


def get_shipyard_name_by_id(fleetmanager, shipyard_id):
    # resp = fleetmanager.db.table("shipyards").select("*").eq("id", shipyard_id).execute().data
    for yard in fleetmanager.cached_tables["shipyards"]:
        if int(yard["id"]) == int(shipyard_id):
            return yard["name"]


def get_hull_number(fleetmanager, ship_id: int):
    # ship_list = fleetmanager.db.table("ships").select("*").execute().data
    ship_list = fleetmanager.cached_tables["ships"]

    models = {}
    same_models = []

    for row in fleetmanager.cached_tables["ship_models"]:
        models[row["id"]] = row["classification"]

    # ship = fleetmanager.db.table("ships").select("*").eq("id", ship_id).execute().data.pop()
    ship = {}
    for _ship in fleetmanager.cached_tables["ships"]:
        if int(_ship["id"]) == int(ship_id):
            ship = _ship
            break


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


def is_valid_ship_model(fleetmanager, ship_model):
    for model in fleetmanager.cached_tables["ship_models"]:
        if int(model["id"]) == int(ship_model):
            return True

    return False


def is_valid_shipyard(fleetmanager, shipyard):
    for yard in fleetmanager.cached_tables["shipyards"]:
        if int(yard["id"]) == int(shipyard):
            return True

    return False


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

