# 60 天教學範例

命名：`dayN_title.py`；title 依範例內容命名，使用英文小寫與底線。

這些是各課可獨立執行的教學範例。正式專案的整合與遠端驗收，依各課教材進行。

在專案根目錄執行單份範例：

```powershell
.\.venv\Scripts\python.exe CourseNotes/CourseExamples/day3_connection_and_result_models.py
```

執行全部教材測試：

```powershell
.\.venv\Scripts\python.exe -m pytest CourseNotes/CourseExamples -q
```

| 課程 | 範例 |
|---|---|
| [Day 1](../Course_Day1.md) | [day1_environment_inspection.py](day1_environment_inspection.py) |
| [Day 2](../Course_Day2.md) | [day2_caller_executor_contract.py](day2_caller_executor_contract.py) |
| [Day 3](../Course_Day3.md) | [day3_connection_and_result_models.py](day3_connection_and_result_models.py) |
| [Day 4](../Course_Day4.md) | [day4_dependency_injection.py](day4_dependency_injection.py) |
| [Day 5](../Course_Day5.md) | [day5_ssh_connection_lifecycle.py](day5_ssh_connection_lifecycle.py) |
| [Day 6](../Course_Day6.md) | [day6_small_command_execution.py](day6_small_command_execution.py) |
| [Day 7](../Course_Day7.md) | [day7_command_output_preservation.py](day7_command_output_preservation.py) |
| [Day 8](../Course_Day8.md) | [day8_exception_chaining.py](day8_exception_chaining.py) |
| [Day 9](../Course_Day9.md) | [day9_operation_and_cleanup_failures.py](day9_operation_and_cleanup_failures.py) |
| [Day 10](../Course_Day10.md) | [day10_deadline_budget.py](day10_deadline_budget.py) |
| [Day 11](../Course_Day11.md) | [day11_dual_stream_collection.py](day11_dual_stream_collection.py) |
| [Day 12](../Course_Day12.md) | [day12_command_deadline_polling.py](day12_command_deadline_polling.py) |
| [Day 13](../Course_Day13.md) | [day13_bounded_output_decoding.py](day13_bounded_output_decoding.py) |
| [Day 14](../Course_Day14.md) | [day14_integration_test_selection.py](day14_integration_test_selection.py) |
| [Day 15](../Course_Day15.md) | [day15_phase_one_acceptance_gate.py](day15_phase_one_acceptance_gate.py) |
| [Day 16](../Course_Day16.md) | [day16_command_line_parsing.py](day16_command_line_parsing.py) |
| [Day 17](../Course_Day17.md) | [day17_tool_exit_status.py](day17_tool_exit_status.py) |
| [Day 18](../Course_Day18.md) | [day18_configuration_precedence.py](day18_configuration_precedence.py) |
| [Day 19](../Course_Day19.md) | [day19_correlated_logging.py](day19_correlated_logging.py) |
| [Day 20](../Course_Day20.md) | [day20_safe_diagnostic_summary.py](day20_safe_diagnostic_summary.py) |
| [Day 21](../Course_Day21.md) | [day21_retry_safety_policy.py](day21_retry_safety_policy.py) |
| [Day 22](../Course_Day22.md) | [day22_bounded_retry.py](day22_bounded_retry.py) |
| [Day 23](../Course_Day23.md) | [day23_backoff_and_jitter.py](day23_backoff_and_jitter.py) |
| [Day 24](../Course_Day24.md) | [day24_fake_clock_testing.py](day24_fake_clock_testing.py) |
| [Day 25](../Course_Day25.md) | [day25_application_boundary_testing.py](day25_application_boundary_testing.py) |
| [Day 26](../Course_Day26.md) | [day26_job_identity_and_ordering.py](day26_job_identity_and_ordering.py) |
| [Day 27](../Course_Day27.md) | [day27_sequential_batch_execution.py](day27_sequential_batch_execution.py) |
| [Day 28](../Course_Day28.md) | [day28_worker_pool_limit.py](day28_worker_pool_limit.py) |
| [Day 29](../Course_Day29.md) | [day29_concurrent_outcome_collection.py](day29_concurrent_outcome_collection.py) |
| [Day 30](../Course_Day30.md) | [day30_per_job_resource_ownership.py](day30_per_job_resource_ownership.py) |
| [Day 31](../Course_Day31.md) | [day31_queue_backpressure.py](day31_queue_backpressure.py) |
| [Day 32](../Course_Day32.md) | [day32_bounded_batch_dispatch.py](day32_bounded_batch_dispatch.py) |
| [Day 33](../Course_Day33.md) | [day33_queue_task_accounting.py](day33_queue_task_accounting.py) |
| [Day 34](../Course_Day34.md) | [day34_cooperative_cancellation.py](day34_cooperative_cancellation.py) |
| [Day 35](../Course_Day35.md) | [day35_atomic_inbox_shutdown.py](day35_atomic_inbox_shutdown.py) |
| [Day 36](../Course_Day36.md) | [day36_shutdown_race_testing.py](day36_shutdown_race_testing.py) |
| [Day 37](../Course_Day37.md) | [day37_remote_batch_test_harness.py](day37_remote_batch_test_harness.py) |
| [Day 38](../Course_Day38.md) | [day38_batch_outcome_validation.py](day38_batch_outcome_validation.py) |
| [Day 39](../Course_Day39.md) | [day39_execution_history_schema.py](day39_execution_history_schema.py) |
| [Day 40](../Course_Day40.md) | [day40_result_repository.py](day40_result_repository.py) |
| [Day 41](../Course_Day41.md) | [day41_transaction_rollback.py](day41_transaction_rollback.py) |
| [Day 42](../Course_Day42.md) | [day42_single_database_writer.py](day42_single_database_writer.py) |
| [Day 43](../Course_Day43.md) | [day43_bounded_history_query.py](day43_bounded_history_query.py) |
| [Day 44](../Course_Day44.md) | [day44_interrupted_job_recovery.py](day44_interrupted_job_recovery.py) |
| [Day 45](../Course_Day45.md) | [day45_atomic_json_export.py](day45_atomic_json_export.py) |
| [Day 46](../Course_Day46.md) | [day46_execution_and_storage_status.py](day46_execution_and_storage_status.py) |
| [Day 47](../Course_Day47.md) | [day47_history_report_roundtrip.py](day47_history_report_roundtrip.py) |
| [Day 48](../Course_Day48.md) | [day48_risk_based_test_matrix.py](day48_risk_based_test_matrix.py) |
| [Day 49](../Course_Day49.md) | [day49_repeatable_benchmark.py](day49_repeatable_benchmark.py) |
| [Day 50](../Course_Day50.md) | [day50_worker_count_benchmark.py](day50_worker_count_benchmark.py) |
| [Day 51](../Course_Day51.md) | [day51_local_bottleneck_profiling.py](day51_local_bottleneck_profiling.py) |
| [Day 52](../Course_Day52.md) | [day52_string_assembly_optimization.py](day52_string_assembly_optimization.py) |
| [Day 53](../Course_Day53.md) | [day53_bounded_memory_observation.py](day53_bounded_memory_observation.py) |
| [Day 54](../Course_Day54.md) | [day54_performance_report_summary.py](day54_performance_report_summary.py) |
| [Day 55](../Course_Day55.md) | [day55_package_metadata.py](day55_package_metadata.py) |
| [Day 56](../Course_Day56.md) | [day56_continuous_integration_commands.py](day56_continuous_integration_commands.py) |
| [Day 57](../Course_Day57.md) | [day57_portable_file_handling.py](day57_portable_file_handling.py) |
| [Day 58](../Course_Day58.md) | [day58_documentation_acceptance_gate.py](day58_documentation_acceptance_gate.py) |
| [Day 59](../Course_Day59.md) | [day59_project_demo_agenda.py](day59_project_demo_agenda.py) |
| [Day 60](../Course_Day60.md) | [day60_release_readiness_gate.py](day60_release_readiness_gate.py) |
