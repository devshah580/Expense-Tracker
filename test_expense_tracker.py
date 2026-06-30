import subprocess
import os

MAIN_FILE = "main.py"
DATA_FILE = "expenses.csv"


def run_command(args):
    result = subprocess.run(
        ["python", MAIN_FILE] + args,
        capture_output=True,
        text=True
    )

    return result.stdout.strip(), result.stderr.strip()


def assert_contains(output, expected):
    if expected not in output:
        raise AssertionError(
            f'Expected "{expected}"\nGot:\n{output}'
        )


def run_test(name, func):
    print(f"Testing {name}...", end=" ")

    try:
        func()
        print("✓")

    except AssertionError as e:
        print("✗")
        raise e


# ---------- REQUIRED FEATURES ----------

def test_add():
    out, err = run_command([
        "add",
        "--description", "Lunch",
        "--amount", "20"
    ])

    assert_contains(out + err, "Expense added")


def test_list():
    out, err = run_command(["list"])

    assert_contains(out, "Lunch")
    assert_contains(out, "20")


def test_summary():
    out, err = run_command(["summary"])

    assert_contains(out, "20")


def test_summary_month():
    out, err = run_command([
        "summary",
        "--month", "6"
    ])

    # Adjust if your wording differs
    assert_contains(out, "20")


def test_update():
    out, err = run_command([
        "update",
        "--id", "1",
        "--amount", "25"
    ])

    assert_contains(out + err, "updated")

    out, err = run_command(["list"])

    assert_contains(out, "25")


def test_delete():
    out, err = run_command([
        "delete",
        "--id", "1"
    ])

    assert_contains(out + err, "deleted")


# ---------- ERROR HANDLING ----------

def test_negative_amount():
    out, err = run_command([
        "add",
        "--description", "Bad",
        "--amount", "-5"
    ])

    assert_contains(out + err, "Invalid Expense Amount")


def test_missing_description():
    out, err = run_command([
        "add",
        "--amount", "10"
    ])

    assert_contains(
        out + err,
        "A description of the expense is required"
    )


def test_invalid_id_delete():
    out, err = run_command([
        "delete",
        "--id", "abc"
    ])

    assert_contains(out + err, "Invalid ID")


def test_nonexistent_id():
    out, err = run_command([
        "delete",
        "--id", "999"
    ])

    assert_contains(out + err, "ID does not exist")


def test_invalid_update_id():
    out, err = run_command([
        "update",
        "--id", "abc",
        "--amount", "10"
    ])

    assert_contains(out + err, "Invalid ID")


def test_invalid_update_amount():
    out, err = run_command([
        "update",
        "--id", "1",
        "--amount", "-10"
    ])

    assert_contains(out + err, "Invalid Expense Amount")


def test_invalid_month():
    out, err = run_command([
        "summary",
        "--month", "13"
    ])

    assert_contains(out + err, "Invalid Month")


def test_invalid_date():
    out, err = run_command([
        "add",
        "--description", "Coffee",
        "--amount", "5",
        "--date", "2026/01/01"
    ])

    assert_contains(
        out + err,
        "Invalid date format"
    )


def main():

    tests = [
        ("add", test_add),
        ("list", test_list),
        ("summary", test_summary),
        ("summary by month", test_summary_month),
        ("update", test_update),

        #("negative amount", test_negative_amount),
        #("missing description", test_missing_description),
        #("invalid delete ID", test_invalid_id_delete),
        #("nonexistent ID", test_nonexistent_id),
        #("invalid update ID", test_invalid_update_id),
        #("invalid update amount", test_invalid_update_amount),
        #("invalid month", test_invalid_month),
        #("invalid date", test_invalid_date),

        ("delete", test_delete),
    ]

    passed = 0

    for name, test in tests:
        try:
            run_test(name, test)
            passed += 1

        except AssertionError as e:
            print("\nTEST FAILED:")
            print(e)
            break

    print(f"\nPassed {passed}/{len(tests)} tests.")


if __name__ == "__main__":
    main()