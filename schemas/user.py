def userEntity(item) -> dict:
    print("Stop itttt")
    print(item)
    return {
        "id": str(item["_id"]),
        "firstName": item["firstName"],
        "lastName": item["lastName"],
        "email": item["email"],
        "password": item["password"],
        "isSuperAdmin": item["isSuperAdmin"],
    }

def usersEntity(entity) -> list:

    data = []
    print(entity)
    # for item in entity:
    #     print(item)
       # data.append(userEntity(item))
    return data