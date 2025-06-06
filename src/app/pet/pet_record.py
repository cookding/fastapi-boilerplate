from tortoise import Model
from tortoise.fields import CharField, DatetimeField

from app.pet.pet_schema import Pet


class PetRecord(Model):
    class Meta:
        table = "pets"

    id = CharField(primary_key=True, max_length=200)
    name = CharField(max_length=200)
    avatar_url = CharField(null=True, max_length=2000)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    def to_entity(self) -> Pet:
        return Pet(
            id=self.id,
            name=self.name,
            avatar_url=self.avatar_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
