import pathlib

print(
    pathlib.Path(
        (pathlib.Path(__file__).parent.parent.parent / "data").resolve()
    ).resolve
)
print((pathlib.Path(__file__).parent.parent.parent / "data").resolve())
