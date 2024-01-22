from pydantic import Field
from dataclasses_avroschema.pydantic import AvroBaseModel


id_description: str = "Used to identify the account"


class ReusedToken(AvroBaseModel):
    id: str = Field(description=id_description)
