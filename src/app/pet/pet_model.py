from tortoise import Model
from tortoise.fields import CharField, DatetimeField

from app.pet.pet_entity import Pet


class PetModel(Model):
    class Meta:
        table = "pets"

    id = CharField(primary_key=True, max_length=200)
    name = CharField(max_length=200)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    def json(self) -> Pet:
        return Pet(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
