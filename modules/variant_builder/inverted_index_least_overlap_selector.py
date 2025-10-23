import uuid
from collections import defaultdict
from math import inf
from typing import override

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.utils.utils import rnd
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.task_selector import QTaskSelector


class IndexedLeastOverlapSelector(QTaskSelector[C, V, Q, A]):
    def __init__(self) -> None:
        self.task_usage_count: dict[uuid.UUID, int] = defaultdict(int)
        self.L: dict[uuid.UUID, set[int]] = defaultdict(set)  # inverted index
        self.variant_task_sets: list[set[uuid.UUID]] = []  # cache per variant
        self._indexed_upto: int = 0  # #variants already indexed

    def _update_index(self, ctx: DynamicCtx[C, V, Q, A]) -> None:
        pv = ctx.previous_variants
        for vidx in range(self._indexed_upto, len(pv)):
            task_ids = {t.id for t in pv[vidx].tasks}
            self.variant_task_sets.append(task_ids)
            for tid in task_ids:
                self.L[tid].add(vidx)
        self._indexed_upto = len(pv)

    @override
    def select(
        self, filtered_tasks: list[QTask[C, V, Q, A]], ctx: DynamicCtx[C, V, Q, A]
    ) -> QTask[C, V, Q, A]:
        rnd.shuffle(filtered_tasks)
        self._update_index(ctx)

        p = self._indexed_upto
        if p == 0:
            best = min(filtered_tasks, key=lambda t: self.task_usage_count[t.id])
            self.task_usage_count[best.id] += 1
            print(0)
            return best

        U_ids = {t.id for t in ctx.current_variant_tasks}
        M = [0] * p
        for tid in U_ids:
            for v in self.L.get(tid, ()):
                M[v] += 1

        Mmax = max(M)
        max_idx = {i for i, val in enumerate(M) if val == Mmax}
        M2 = max((val for i, val in enumerate(M) if i not in max_idx), default=-inf)

        def score(task: QTask[C, V, Q, A]) -> int:
            tid = task.id
            in_variants = self.L.get(tid, set())
            if not in_variants:
                return Mmax

            max_in = max(M[v] for v in in_variants) + 1
            has_max_outside = len(max_idx - in_variants) > 0
            max_out = Mmax if has_max_outside else M2
            return max(max_in, max_out)

        best_score = inf
        best_candidates: list[QTask[C, V, Q, A]] = []
        for task in filtered_tasks:
            s = score(task)
            if s < best_score:
                best_score = s
                best_candidates = [task]
            elif s == best_score:
                best_candidates.append(task)

        chosen = min(best_candidates, key=lambda t: self.task_usage_count[t.id])
        self.task_usage_count[chosen.id] += 1

        print(best_score)
        return chosen
