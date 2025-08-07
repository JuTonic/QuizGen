from modules.tag import Tag
from modules.task import QTask
from modules.task.factory import QTaskFactory
from modules.variant_builder import VariantFactory
from modules.variant_builder.task_pool import QTaskPool

tasks_on_first_topic = [QTask(f"1.{i + 1}", tags=Tag("topic", "1")) for i in range(5)]
tasks_on_second_topic = [QTask(f"2.{i + 1}", tags=Tag("topic", "2")) for i in range(5)]
tasks_on_third_topic = [QTask(f"3.{i + 1}", tags=Tag("topic", "3")) for i in range(5)]
tasks_on_forth_topic = [QTask(f"4.{i + 1}", tags=Tag("topic", "4")) for i in range(5)]
tasks_on_fifth_topic = [QTask(f"5.{i + 1}", tags=Tag("topic", "5")) for i in range(5)]
tasks_on_sixth_topic = [QTask(f"6.{i + 1}", tags=Tag("topic", "6")) for i in range(5)]
tasks_on_seventh_topic = [QTask(f"7.{i + 1}", tags=Tag("topic", "7")) for i in range(5)]

task_pool = QTaskPool(
    tasks_on_first_topic
    + tasks_on_second_topic
    + tasks_on_third_topic
    + tasks_on_forth_topic
    + tasks_on_fifth_topic
    + tasks_on_sixth_topic
    + tasks_on_seventh_topic
)

vf = VariantFactory(number_of_tasks=7, task_pool=task_pool)

_ = vf.task[0].must.include_tag("topic", "1")
_ = vf.task[1].must.include_tag("topic", "2")
_ = vf.task[2].must.include_tag("topic", "3")
_ = vf.task[3].must.include_tag("topic", "4")
_ = vf.task[4].must.include_tag("topic", "5")
_ = vf.task[5].must.include_tag("topic", "6")
_ = vf.task[6].must.include_tag("topic", "7")

variants = vf.generate_variants(number_of_variants=30)

i = 0
for variant in variants:
    print(f"Variant {i + 1}:")
    print(*[task.question for task in variant.tasks])
    i += 1
