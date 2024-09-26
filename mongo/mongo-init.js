db = db.getSiblingDB("admin");
db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

db = db.getSiblingDB("User_DB");
db.createUser(
    {
        user: process.env.MONGO_INITDB_ROOT_USERNAME,
        pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
        roles: [
            {
                role: "dbOwner",
                db: "User_DB",
            }
        ]
    }
)
db.createCollection('init');
db.createCollection('users');