def get_severity(violation_type):
    if violation_type == "no_helmet":
        return "Medium"
    elif violation_type == "triple_riding":
        return "High"
    elif violation_type == "red_light_jump":
        return "High"
    elif violation_type == "overspeed":
        return "Medium"
    else:
        return "Low"


if __name__ == "__main__":
    test_violations = [
        "no_helmet",
        "triple_riding",
        "red_light_jump",
        "overspeed",
        "lane_violation"
    ]

    for v in test_violations:
        print(v, "=> Severity:", get_severity(v))
