"""Traduz block states do schematic em itens que o jogador precisa ter."""

from litemapy import BlockState

NS: str = "minecraft:"

# Sem item, ou impossível de obter em survival
SKIP: frozenset[str] = frozenset(
    {
        "air",
        "cave_air",
        "void_air",
        "structure_void",
        "water",
        "lava",
        "bubble_column",
        "fire",
        "soul_fire",
        "powder_snow",
        "frosted_ice",
        "piston_head",
        "moving_piston",
        "nether_portal",
        "end_portal",
        "end_gateway",
        "end_portal_frame",
        "spawner",
        "trial_spawner",
        "vault",
        "command_block",
        "chain_command_block",
        "repeating_command_block",
        "structure_block",
        "jigsaw",
        "barrier",
        "light",
        "bedrock",
        "reinforced_deepslate",
        "budding_amethyst",
        "petrified_oak_slab",
        "frogspawn",
        "test_block",
        "test_instance_block",
    }
)

# Bloco cujo item tem outro nome (inclui ids de versões antigas)
RENAME: dict[str, str] = {
    "grass": "short_grass",
    "grass_path": "dirt_path",
    "chain": "iron_chain",
    "wall_torch": "torch",
    "soul_wall_torch": "soul_torch",
    "redstone_wall_torch": "redstone_torch",
    "redstone_wire": "redstone",
    "tripwire": "string",
    "farmland": "dirt",
    "water_cauldron": "cauldron",
    "lava_cauldron": "cauldron",
    "powder_snow_cauldron": "cauldron",
    "bamboo_sapling": "bamboo",
    "kelp_plant": "kelp",
    "tall_seagrass": "seagrass",
    "cave_vines": "glow_berries",
    "cave_vines_plant": "glow_berries",
    "weeping_vines_plant": "weeping_vines",
    "twisting_vines_plant": "twisting_vines",
    "big_dripleaf_stem": "big_dripleaf",
    "sweet_berry_bush": "sweet_berries",
    "cocoa": "cocoa_beans",
    "wheat": "wheat_seeds",
    "carrots": "carrot",
    "potatoes": "potato",
    "beetroots": "beetroot_seeds",
    "melon_stem": "melon_seeds",
    "attached_melon_stem": "melon_seeds",
    "pumpkin_stem": "pumpkin_seeds",
    "attached_pumpkin_stem": "pumpkin_seeds",
    "torchflower_crop": "torchflower_seeds",
    "pitcher_crop": "pitcher_pod",
}

# Variante "na parede" -> item normal
SUFFIX: list[tuple[str, str]] = [
    ("_wall_hanging_sign", "_hanging_sign"),
    ("_wall_sign", "_sign"),
    ("_wall_banner", "_banner"),
    ("_wall_fan", "_fan"),
    ("_wall_skull", "_skull"),
    ("_wall_head", "_head"),
]

# Vaso: o nome da planta dentro nem sempre é o do item
POTTED: dict[str, str] = {
    "azalea_bush": "azalea",
    "flowering_azalea_bush": "flowering_azalea",
}


def is_second_half(state: BlockState) -> bool:
    """Portas e plantas altas (half) e camas (part) ocupam dois blocos; conta só um."""
    upper: bool = "half" in state and state["half"] == "upper"
    foot: bool = "part" in state and state["part"] == "foot"
    return upper or foot


def to_items(state: BlockState) -> list[str]:
    if is_second_half(state):
        return []

    name: str = state.id.removeprefix(NS)

    if name in SKIP:
        return []

    if name in RENAME:
        return [NS + RENAME[name]]

    if name.startswith("potted_"):
        plant: str = name.removeprefix("potted_")
        return [NS + "flower_pot", NS + POTTED.get(plant, plant)]

    if name.endswith("_candle_cake"):
        candle: str = name.removesuffix("_cake")
        return [NS + "cake", NS + candle]

    if name == "candle_cake":
        return [NS + "cake", NS + "candle"]

    if name.startswith("infested_"):
        return [NS + name.removeprefix("infested_")]

    # Encerar é bloco + favo; o jogador entrega o cobre sem cera
    if name.startswith("waxed_"):
        return [NS + name.removeprefix("waxed_"), NS + "honeycomb"]

    for block_suffix, item_suffix in SUFFIX:
        if name.endswith(block_suffix):
            return [NS + name.removesuffix(block_suffix) + item_suffix]

    return [state.id]
