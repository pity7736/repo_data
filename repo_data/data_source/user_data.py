from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    data_source_id: str
    name: str = None
    company: str = None
    blog: str = None
    location: str = None
    email: str = None
    bio: str = None
