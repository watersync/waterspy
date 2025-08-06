def handle_if_below_detection_limit(value: float) -> float:
    """Returns the 0 if the value is either 9999 or -9999."""
    return 0 if value in [float(9999), float(-9999)] else value
