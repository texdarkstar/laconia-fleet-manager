
def get_model_id_by_name(fleetmanager, model):
    return fleetmanager.ship_models[model]['id']


def get_shipyard_id(fleetmanager, shipyard):
    return fleetmanager.shipyards[shipyard]['id']


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

    n = str(same_models.index(ship["id"]) + 1)

    if int(n) < 10:
        n = "0" + n

    hull_string = models[ship["model_id"]] + "-" + n


    return hull_string


def new_hull(fleetmanager, model):
    model_id = get_model_id_by_name(fleetmanager, model)
    hull_number = fleetmanager.ship_models[model]['classification']

    ships = fleetmanager.db.table("ships").select("*").eq("model_id", model_id).execute().data

    n = str(len(ships) + 1)

    if int(n) < 10:
        n = "0" + n

    hull_number += "-" + n

    return hull_number
