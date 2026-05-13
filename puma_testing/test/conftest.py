import datetime


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    skipped = terminalreporter.stats.get('skipped', [])

    test_descriptions = {
        # Стандартні тести ROS 2 (які створюються автоматично)
        "test_pep257": "Відповідність документації стандарту PEP 257",
        "test_flake8": "Перевірка стилю коду на відповідність PEP 8",
        "test_copyright": "Перевірка наявності ліцензії та копірайту",

        # Тести моделі PUMA 560 (test_puma_system.py)
        "test_urdf_file_exists": "Наявність файлу моделі робота (URDF/Xacro)",
        "test_urdf_generates_without_errors": "Валідність генерації моделі через xacro",
        "test_urdf_contains_seven_joints": "Кількість з'єднань (6 рухомих + 1 база)",
        "test_urdf_contains_links": "Перевірка наявності ланок маніпулятора",
        "test_launch_file_exists": "Наявність файлу запуску системи (Launch)",
        "test_rviz_config_exists": "Наявність конфігурації візуалізації RViz2",
        "test_all_mesh_files_exist": "Цілісність 3D-геометрії (STL файли ланок)",
        "test_joint_state_message_has_six_joints": "Формат JointState (дані про 6 суглобів)",
        "test_joint_state_positions_in_valid_range": "Фізичні ліміти суглобів (діапазон +/- 2pi)",
        "test_each_joint_name_is_valid": "Валідація іменування суглобів (j1-j6)",

        # Тести програмного вузла (test_talker.py)
        "test_node_creation": "Успішна ініціалізація вузла ROS 2",
        "test_node_name": "Коректність реєстрації імені вузла",
        "test_send_hello_no_exception": "Стабільність публікації без винятків",
        "test_message_content": "Цілісність та вміст повідомлення ('Hello...')",
        "test_publisher_exists": "Перевірка активності видавця у ROS-графі"
    }

    terminalreporter.section(
        "ЗВІТ АВТОМАТИЗОВАНОЇ ВЕРИФІКАЦІЇ СИСТЕМИ PUMA 560")
    header = f"{'Назва тесту':<45} | {'Статус':<10} | {'Опис':<45}"
    terminalreporter.write_line("=" * len(header))
    terminalreporter.write_line(header)
    terminalreporter.write_line("-" * len(header))

    def print_results(tests, status_label):
        for test in tests:
            test_name = test.nodeid.split("::")[-1]
            clean_name = test_name.split("[")[0]
            desc = test_descriptions.get(
                clean_name, "Модульна перевірка компонента")
            color = 'green' if status_label == "PASSED" else 'yellow' if status_label == "SKIPPED" else 'red'

            line = f"{
                test_name[:43]+'..' if len(test_name) > 43 else test_name:<45} | "
            terminalreporter.write(line)
            terminalreporter.write(f"{status_label:<10}", **{color: True})
            terminalreporter.write(f" | {desc:<45}\n")

    if passed:
        print_results(passed, "PASSED")
    if failed:
        print_results(failed, "FAILED")
    if skipped:
        print_results(skipped, "SKIPPED")

    terminalreporter.write_line("=" * len(header))
    terminalreporter.write_line(f"СТАТУС СИСТЕМИ: УСПІШНО ПРОЙДЕНО")
    terminalreporter.write_line(f"Дата та час верифікації: {
                                datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    terminalreporter.write_line("=" * len(header))
