from collections.abc import Iterable
from typing import Generic

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant import QVariant
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.default_task_selector import LeastUsedTaskSelector
from modules.variant_builder.filters import Filter
from modules.variant_builder.task_pool import QTaskPool
from modules.variant_builder.task_selector import QTaskSelector
from modules.variant_builder.variant_set import QVariantSet
from modules.variant_builder.variant_task import VariantTask


class VariantFactory(Generic[C, V, Q, A]):
    task_pool: QTaskPool[C, V, Q, A]
    previous_variants: QVariantSet[C, V, Q, A] = QVariantSet()
    task_selector: QTaskSelector[C, V, Q, A]
    task: list[VariantTask[C, V, Q, A]]
    number_of_tasks: int

    def __init__(
        self,
        number_of_tasks: int,
        task_pool: Iterable[QTask[C, V, Q, A]],
        task_selector: QTaskSelector[C, V, Q, A] | None = None,
    ):
        self.task = [VariantTask() for _ in range(number_of_tasks)]
        self.number_of_tasks = number_of_tasks
        self.task_pool = QTaskPool[C, V, Q, A](task_pool)
        self.task_selector = (
            task_selector if task_selector is not None else LeastUsedTaskSelector()
        )

    def generate_variants(self, number_of_variants: int) -> QVariantSet[C, V, Q, A]:
        variant_task_filters: list[Filter[C, V, Q, A]] = [
            b.must.build() for b in self.task
        ]
        static_filter_matches_per_task = self._get_static_filter_matches(
            variant_task_filters
        )

        dynamic_context = DynamicCtx(
            self.task_pool,
        )

        for _ in range(number_of_variants):
            variant_tasks: list[QTask[C, V, Q, A]] = []
            for task_index in range(self.number_of_tasks):
                dynamic_filtered_matches = self._get_dynamic_filter_matches(
                    static_filter_matches_per_task[task_index],
                    variant_task_filters[task_index],
                    dynamic_context,
                )

                selected_task = self.task_selector.select(
                    dynamic_filtered_matches, dynamic_context
                )
                variant_tasks.append(selected_task)
                dynamic_context.current_variant_tasks.append(selected_task)

            variant = QVariant(variant_tasks)
            dynamic_context.previous_variants.append(variant)
            dynamic_context.current_variant_tasks.clear()

        return dynamic_context.previous_variants

    def _get_static_filter_matches(
        self, task_filters: list[Filter[C, V, Q, A]]
    ) -> list[list[QTask[C, V, Q, A]]]:
        statical_filter_matches_per_task: list[list[QTask[C, V, Q, A]]] = [
            [] for _ in range(self.number_of_tasks)
        ]

        for task in self.task_pool:
            task_filter_index = 0
            for filter in task_filters:
                if filter.static.is_satisfied(task):
                    statical_filter_matches_per_task[task_filter_index].append(task)
                task_filter_index += 1

        return statical_filter_matches_per_task

    def _get_dynamic_filter_matches(
        self,
        statically_filtered_pool: list[QTask[C, V, Q, A]],
        filter: Filter[C, V, Q, A],
        ctx: DynamicCtx[C, V, Q, A],
    ) -> list[QTask[C, V, Q, A]]:
        dynamic_filter_matches: list[QTask[C, V, Q, A]] = []

        for task in statically_filtered_pool:
            if filter.dynamic.check_if_satisfied(task, ctx):
                dynamic_filter_matches.append(task)

        return dynamic_filter_matches
