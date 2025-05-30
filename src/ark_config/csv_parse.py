import csv
from typing import Iterable, Callable, Optional
from collections import defaultdict
from os import PathLike

from src.complex_values import ConfigOverrideSupplyCrateItems


def get_bool(value: str) -> Optional[bool]:
    if value.strip() == '':
        return None
    return value == "TRUE"


def get_int(value: str) -> Optional[int]:
    if value.strip() == '':
        return None
    value = value.replace(',', '.')
    value = value.replace('\xa0', '')
    return int(float(value))


def get_float(value: str) -> Optional[float]:
    if value.strip() == '':
        return None
    value = value.replace(',', '.')
    value = value.replace('\xa0', '')
    return float(value)


def get_str_list(value: str, sep: Optional[str] = ',') -> list[str]:
    return [s.strip() for s in value.split(sep)]


TYPE_MAP = {
    # supply crate
    'MinItemSets': get_int,
    'MaxItemSets': get_int,
    'bSetsRandomWithoutReplacement': get_bool,
    'bAppendItemSets': get_bool,

    # item sets
    '_SetWeight': get_float,
    '_MinNumItems': get_int,
    '_MaxNumItems': get_int,
    '_bItemsRandomWithoutReplacement': get_bool,

    # item entries
    '__EntryWeight': get_float,
    '__ItemClassStrings': get_str_list,
    '__ItemsWeights': lambda x: [get_float(i) for i in get_str_list(x, ';')],
    '__MinQuantity': get_float,
    '__MaxQuantity': get_float,
    "__MinQuality": get_float,
    "__MaxQuality": get_float,
    "__bForceBlueprint": get_bool,
    "__ChanceToBeBlueprintOverride": get_float,
}

SUPPLY_CRATE_KEYS = [
    "SupplyCrateClassString(s)",
    "MinItemSets",
    "MaxItemSets",
    "bSetsRandomWithoutReplacement",
    "bAppendItemSets",
]

ITEM_SETS_KEYS = [
    "_SetWeight",
    "_MinNumItems",
    "_MaxNumItems",
    "_bItemsRandomWithoutReplacement",
]

ITEM_ENTRIES_KEYS = [
    "__EntryWeight",
    "__ItemClassStrings",
    "__ItemsWeights",
    "__MinQuantity",
    "__MaxQuantity",
    "__MinQuality",
    "__MaxQuality",
    "__bForceBlueprint",
    "__ChanceToBeBlueprintOverride",
]


def all_not_empty(data: dict, keys: Iterable) -> bool:
    keys = set(keys)
    values = [data.get(k) for k in keys]
    return all(v != "" for v in values)


def parse_values(
    rows: list[dict[str, str]],
    type_map: dict[str, Callable]
) -> list[dict]:
    def convert_value(key: str, value):
        if key in type_map:
            return type_map[key](value)
        return value

    return [{
        k: convert_value(k, v) for k, v in row.items()} for row in rows]


def ffill(rows: list[dict], keys: list[str]) -> list[dict]:
    result = []
    current_values = None

    for i, row in enumerate(rows):
        if all_not_empty(row, keys):
            current_values = {k: v for k, v in row.items() if k in keys}

        if current_values is None:
            raise KeyError(
                f"Row {i+1}:")

        result.append(row | current_values)

    return result


def csv_to_supply_crate_items(
    filepath: str | PathLike
) -> list[ConfigOverrideSupplyCrateItems]:

    with open(filepath, encoding='utf-8', newline="") as f:
        rows = list(csv.DictReader(f))

    all_keys = set(SUPPLY_CRATE_KEYS + ITEM_SETS_KEYS + ITEM_ENTRIES_KEYS)
    rows_filtered = [{k: v for k, v in row.items() if k in all_keys}
                     for row in rows]
    rows_ffilled = ffill(rows_filtered, SUPPLY_CRATE_KEYS)
    rows_ffilled = ffill(rows_ffilled, ITEM_SETS_KEYS)
    rows_parsed = parse_values(rows_ffilled, TYPE_MAP)

    supply_crate_items = defaultdict(lambda: defaultdict(list))

    for row in rows_parsed:
        supply_crate_keys = [v for k, v in row.items(
        ) if k in SUPPLY_CRATE_KEYS and k != 'SupplyCrateClassString(s)']

        supply_crate_cls_raw: str = row['SupplyCrateClassString(s)']
        supply_crate_cls_strs = [
            cls_str.strip() for cls_str in supply_crate_cls_raw.split(',')]

        item_set_keys = [v for k, v in row.items() if k in ITEM_SETS_KEYS]
        item_set = tuple(item_set_keys)

        for cls_str in supply_crate_cls_strs:
            supply_crate = tuple([cls_str, *supply_crate_keys])
            item_entry = {k: v for k,
                          v in row.items() if k in ITEM_ENTRIES_KEYS}
            supply_crate_items[supply_crate][item_set].append(item_entry)

    result = []
    current_supply_crate_items = None
    current_item_set = None

    for supply_crate_items_args, item_sets in supply_crate_items.items():
        supply_crate_items_keys = ['SupplyCrateClassString'] + \
            [i for i in SUPPLY_CRATE_KEYS if i != 'SupplyCrateClassString(s)']
        current_supply_crate_items = dict(
            zip(supply_crate_items_keys, supply_crate_items_args))
        current_supply_crate_items['NumItemSetsPower'] = 1.0
        current_supply_crate_items['ItemSets'] = []

        for item_set_args, item_entries in item_sets.items():
            item_set_keys = [i.lstrip('_') for i in ITEM_SETS_KEYS]
            current_item_set = dict(zip(item_set_keys, item_set_args))
            current_item_set['NumItemsPower'] = 1.0
            current_item_set['ItemEntries'] = []
            current_supply_crate_items['ItemSets'].append(current_item_set)

            for item_entry_raw in item_entries:
                item_entry = {k.lstrip('__'): v for k,
                              v in item_entry_raw.items()}
                current_item_set['ItemEntries'].append(item_entry)

        supply_crate_items = ConfigOverrideSupplyCrateItems.from_dict(
            current_supply_crate_items)
        result.append(supply_crate_items)

    return result
