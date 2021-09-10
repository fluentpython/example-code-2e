from dataclasses import dataclass

# tag::CLUBMEMBER[]
@dataclass
class ClubMember:
    name: str
    guests: list = []
# end::CLUBMEMBER[]
