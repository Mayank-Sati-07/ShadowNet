import subprocess


scripts = [
    "inventory.py",
    "inventory_summary.py",
    "normalize_persons.py",
    "normalize_phones.py",
    "normalize_vehicles.py",
    "normalize_locations.py",
    "normalize_organizations.py",
    "normalize_accounts.py",
    "normalize_firs.py",
    "normalize_calls.py",
    "normalize_emails.py",
    "normalize_transactions.py",
    "normalize_visits.py",
    "combine_relationships.py",
    "validate_relationships.py",
]


for script in scripts:

    print()
    print("=" * 60)
    print(f"Running {script}")
    print("=" * 60)

    result = subprocess.run(
        ["python", f"scripts/{script}"]
    )

    if result.returncode != 0:

        print(
            f"Pipeline stopped at {script}"
        )

        break