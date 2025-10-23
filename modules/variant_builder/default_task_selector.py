import uuid
from math import inf
from typing import override

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.utils.utils import rnd
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.task_selector import QTaskSelector


class LeastUsedTaskSelector(QTaskSelector[C, V, Q, A]):
    task_usage_count: dict[uuid.UUID, int]

    def __init__(self):
        self.task_usage_count = {}

    @override
    def select(
        self, filtered_tasks: list[QTask[C, V, Q, A]], ctx: DynamicCtx[C, V, Q, A]
    ) -> QTask[C, V, Q, A]:
        rnd.shuffle(filtered_tasks)

        task_scores: list[int] = []

        min_max_intersections = inf
        for task in filtered_tasks:
            max_intersections = 0
            for variant in ctx.previous_variants:
                intersections = 0
                for t in ctx.current_variant_tasks:
                    if t in variant.tasks:
                        intersections += 1
                if task in variant.tasks:
                    intersections += 1
                if intersections > max_intersections:
                    max_intersections = intersections
            task_scores.append(max_intersections)
            if min_max_intersections > max_intersections:
                min_max_intersections = max_intersections

        best_candidates: list[QTask[C, V, Q, A]] = []

        for task, score in zip(filtered_tasks, task_scores):
            if score == min_max_intersections:
                best_candidates.append(task)

        least_used_score = inf
        least_used_task: QTask[C, V, Q, A] = best_candidates[0]

        for task in best_candidates:
            if self.task_usage_count.setdefault(task.id, 0) < least_used_score:
                least_used_score = self.task_usage_count[task.id]
                least_used_task = task

        self.task_usage_count[least_used_task.id] += 1

        print(min_max_intersections)

        return least_used_task
