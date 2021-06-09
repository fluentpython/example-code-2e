# tag::TRASH_TYPES[]
from typing import TypeVar, Generic

class Refuse:  # <1>
    """Any refuse."""

class Biodegradable(Refuse):
    """Biodegradable refuse."""

class Compostable(Biodegradable):
    """Compostable refuse."""

T_contra = TypeVar('T_contra', contravariant=True)  # <2>

class TrashCan(Generic[T_contra]):  # <3>
    def put(self, refuse: T_contra) -> None:
        """Store trash until dumped."""

def deploy(trash_can: TrashCan[Biodegradable]):
    """Deploy a trash can for biodegradable refuse."""
# end::TRASH_TYPES[]


################################################ contravariant trash can


# tag::DEPLOY_TRASH_CANS[]
bio_can: TrashCan[Biodegradable] = TrashCan()
deploy(bio_can)

trash_can: TrashCan[Refuse] = TrashCan()
deploy(trash_can)
# end::DEPLOY_TRASH_CANS[]


################################################ more specific trash can

# tag::DEPLOY_NOT_VALID[]
compost_can: TrashCan[Compostable] = TrashCan()
deploy(compost_can)
## mypy: Argument 1 to "deploy" has
## incompatible type "TrashCan[Compostable]"
##          expected "TrashCan[Biodegradable]"
# end::DEPLOY_NOT_VALID[]
