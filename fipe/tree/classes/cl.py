from typing import Generic

import numpy as np

from ...feature import FeatureEncoder
from ...typing import HV, MNumber, ParsableTreeSKL
from .skl import TreeSKL


class TreeCL(TreeSKL[MNumber], Generic[HV]):
    _voting: HV

    def __init__(
        self,
        tree: ParsableTreeSKL,
        encoder: FeatureEncoder,
        voting: HV,
    ) -> None:
        self._voting = voting
        super().__init__(tree=tree, encoder=encoder)

    def _read_leaf(self, tree: ParsableTreeSKL, node: int) -> None:
        value = tree.value[node].flatten()
        value = np.asarray(value)
        if self._voting:
            k = value.size
            q = np.argmax(value)
            value = np.eye(k)[q]
        self._set_leaf(node=node, value=value)
