from abc import ABC


class Event(ABC):
    """
    Abstract class defining the general structure of a logged event.
    Inherit this class to prepare specific event structures for various logs.

    Attributes:
    - `timestamp`: `int`
    - `hostname`: `str`
    - `process`: `str`
    - `pid`: `int`
    - `action`: `str`
    - `raw_content`: `str`
    """

    def __init__(self, **kwargs) -> None:
        _defaults = {
            "timestamp": None,
            "action": None,
            "raw_content": None,
        }

        for attr, def_value in _defaults.items():
            setattr(self, attr, kwargs.get(attr, def_value))

    def __str__(self) -> str:
        _obj_state = [f"{attr}: {value}" for attr, value in self.__dict__.items()]
        return "{\n\t" + "\n\t".join(_obj_state) + "}"
