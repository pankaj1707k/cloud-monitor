from rich.table import Table

from attestation_agent.utils import console


class AttestationError(Exception):
    def __init__(self, title="AttestationError", msg="generic logging error", **kwargs):
        super().__init__(msg)
        self.title = title
        self.kwargs = kwargs

    def __str__(self) -> str:
        with console.capture() as capture:
            table = Table(
                *self.kwargs.keys(),
                title=self.title
            )

            table.add_row(*map(lambda attr: str(attr), self.kwargs.values()))
            console.print(table)

        return capture.get()


class LogError(AttestationError):
    """
    Generic failure of a logger.
    """

    def __init__(self, title="LogError", msg="generic logging error", **kwargs):
        super().__init__(title, msg, **kwargs)


class ParseError(AttestationError):
    """
    Generic failure of a parser.
    """

    def __init__(self, title="ParseError", msg="generic parse error", **kwargs):
        super().__init__(title, msg, **kwargs)
