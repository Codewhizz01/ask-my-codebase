import os

LEVELS = {"public": 0, "staff": 1, "admin": 2}
ROLE_LEVEL = {"guest": 0, "staff": 1, "admin": 2}

def access_of(path):
    p = path.replace("\\", "/").lower()
    name = os.path.basename(p)
    # secrets, database setup and login logic
    if "/config/" in p or "/migrations/" in p or name in ("authcontroller.js","readme.md"):
        return "admin"
    # public API surface and practice files
    if "/routes/" in p or name.endswith("practice.js"):
        return "public"
    # everything else (controllers, models, app.js, README, package.json)
    return "staff"

def allowed(role, path):
    return LEVELS[access_of(path)] <= ROLE_LEVEL[role]