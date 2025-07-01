from typing import Union

from src.complex_values import (
    ConfigAddNPCSpawnEntriesContainer,
    ConfigOverrideItemMaxQuantity,
    ConfigOverrideSupplyCrateItems,
)


ArkConfigPrimitiveValue = Union[str, int, float, bool]
ArkConfigComplexValue = Union[
    ConfigOverrideSupplyCrateItems,
    ConfigOverrideItemMaxQuantity,
    ConfigAddNPCSpawnEntriesContainer
]
ArkConfigValue = Union[
    Union[ArkConfigPrimitiveValue, ArkConfigComplexValue],
    list[Union[ArkConfigPrimitiveValue, ArkConfigComplexValue]]
]
