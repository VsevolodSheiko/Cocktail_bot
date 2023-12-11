from peewee import SqliteDatabase, Model, CharField, BigIntegerField, PrimaryKeyField

db = SqliteDatabase('db.sqlite3')

# Define a base model class that other models will inherit from
class BaseModel(Model):
    class Meta:
        database = db


class Cocktail(BaseModel):
    id = PrimaryKeyField()
    telegram_id = BigIntegerField()
    name = CharField()
    recipe = CharField(null=True)
    photo = CharField(null=True)
    ingredients = CharField()


def insert_cocktail(telegram_id, name, recipe, photo, ingredients):
    db.connect()

    Cocktail.create(telegram_id=telegram_id, name=name, recipe=recipe, photo=photo, ingredients=ingredients)
    
    db.commit()
    db.close()


def get_favourite_cocktails(telegram_id):
    db.connect()
    result = []
    cocktails = Cocktail.select().where(Cocktail.telegram_id == telegram_id)
    for cocktail in cocktails:
        result.append({
            "id": cocktail.id,
            "telegram_id": cocktail.telegram_id,
            "name": cocktail.name,
            "recipe": cocktail.recipe,
            "photo": cocktail.photo,
            "ingredients": cocktail.ingredients 
        })
    db.close()
    
    return result


def delete_cocktail(id):
    db.connect()
    
    Cocktail.delete_by_id(id)
    
    db.commit()
    db.close()

def create_table():
    db.connect()
    
    Cocktail.create_table()
    
    db.close()

create_table()