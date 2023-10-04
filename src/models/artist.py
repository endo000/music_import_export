class Artist:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Artist({str(self)})"
