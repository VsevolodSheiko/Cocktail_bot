from peewee import SqliteDatabase, Model, CharField, IntegerField

# Define your database - replace 'example.db' with your desired database name
db = SqliteDatabase('db.sqlite3')

# Define a base model class that other models will inherit from
class BaseModel(Model):
    class Meta:
        database = db


class Cocktail(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    difficulty = CharField()
    portion = CharField()
    method = CharField()
    ingredients = CharField()
    photo = CharField()


def insert_cocktail(id, name, difficulty, portion, method, ingredients, photo):
    db.connect()

    Cocktail.create(id=id, name=name, difficulty=difficulty, portion=portion, method=method, ingredients=ingredients, photo=photo)
    db.commit()
    db.close()


def get_cocktail(id):
    db.connect()
    cocktail = Cocktail.get_or_none(Cocktail.id == id)
    db.close()
    
    return [
        cocktail.id, cocktail.name, cocktail.difficulty, cocktail.portion, cocktail.method, cocktail.ingredients, cocktail.photo
    ] if cocktail is not None else None


def get_all_cocktails():
    db.connect()

    result = []
    
    cocktails = Cocktail.select()
    
    for cocktail in cocktails:
        row = [
            cocktail.name,
            cocktail.difficulty,
            cocktail.portion,
            cocktail.method,
            cocktail.ingredients,
            cocktail.photo
        ]
        result.append(row)
    return result
    


