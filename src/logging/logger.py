import csv
from datetime import datetime
from severity import get_severity


def log_violation(plate_number, violation_type):
    severity = get_severity(violation_type)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("violations.csv", "a", newline="") as file:
        writer = csv.writer(file)

        # Write header if file is empty
        if file.tell() == 0:
            writer.writerow([
                "Plate Number",
                "Violation Type",
                "Severity",
                "Timestamp"
            ])

        writer.writerow([
            plate_number,
            violation_type,
            severity,
            timestamp
        ])


# Test logging
if __name__ == "__main__":
    log_violation("UP32AB1234", "no_helmet")
    log_violation("DL01CD5678", "triple_riding")
    log_violation("MH12EF9012", "red_light_jump")

    print("Violations logged successfully.")
