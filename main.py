import json
import os
from collections import Counter
from pathlib import Path

from litemapy import Schematic

from items import to_items

BASE_DIR: Path = Path(__file__).resolve().parent
SCHEMATIC_DIR: Path = BASE_DIR / "schematics"
OUTPUT: Path = BASE_DIR / "catalog.json"

EXTENSION: str = ".litematic"

Recipe = dict[str, int]
Catalog = dict[str, Recipe]


def list_schematics(directory: Path) -> list[Path]:
    return sorted(directory.glob(f"*{EXTENSION}"))


def count_blocks(schematic: Schematic) -> Counter[str]:
    counts: Counter[str] = Counter()

    for region in schematic.regions.values():
        for x in region.xrange():
            for y in region.yrange():
                for z in region.zrange():
                    counts.update(to_items(region[x, y, z]))

    return counts


def build_recipe(path: Path) -> Recipe:
    schematic: Schematic = Schematic.load(str(path))
    counts: Counter[str] = count_blocks(schematic)
    return dict(sorted(counts.items()))


def build_catalog(directory: Path) -> Catalog:
    catalog: Catalog = {}

    for path in list_schematics(directory):
        name: str = path.stem
        recipe: Recipe = build_recipe(path)
        catalog[name] = recipe
        print(f"{name}: {sum(recipe.values())} blocos")

    return catalog


def write_catalog(catalog: Catalog, output: Path) -> None:
    with output.open("w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")


def main() -> None:
    catalog: Catalog = build_catalog(SCHEMATIC_DIR)
    write_catalog(catalog, OUTPUT)


if __name__ == "__main__":
    main()