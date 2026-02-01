"""Generate a short blog post about the benefits of test driving a car.

This script provides a `generate_blog_post()` function that returns a formatted
blog post string and prints it when run as a script.
"""

from __future__ import annotations


def generate_blog_post() -> str:
    """Return a formatted blog post about the benefits of test driving a car."""

    introduction = (
        "When it comes to purchasing a new car, taking a test drive is an essential "
        "step in the decision-making process. Not only does it allow you to experience "
        "the vehicle firsthand, but it also provides valuable insights that help you make "
        "an informed choice."
    )

    benefits = [
        "Experience the Ride: A test drive gives you the opportunity to feel how the car handles on the road. "
        "You can assess acceleration, braking, and overall comfort.",

        "Evaluate Comfort and Features: During a test drive, you can explore the car's interior features "
        "such as seating comfort, infotainment systems, and visibility to determine whether it meets your preferences.",

        "Assess Practicality: A test drive lets you evaluate the car's practicality for daily life — parking ease, cargo space, "
        "and how it fits your lifestyle.",

        "Identify Potential Issues: Taking a car for a test drive can help you spot potential issues — listen for unusual noises, "
        "check for vibrations, and confirm systems are functioning properly.",

        "Build Confidence: A test drive boosts confidence in your decision by letting you experience the vehicle firsthand "
        "and verify it meets your expectations."
    ]

    conclusion = (
        "In conclusion, test driving a car is a crucial step in the car-buying process. "
        "It helps you experience the vehicle, evaluate its features, assess practicality, "
        "identify potential issues, and build confidence in your decision. Before making "
        "your final choice, be sure to take that car for a spin!"
    )

    parts = [introduction, ""]
    parts.extend(f"- {b}" for b in benefits)
    parts.append("")
    parts.append(conclusion)

    return "\n\n".join(parts)


def _run_demo() -> None:
    """Print the generated blog post (used when running the script directly)."""
    print(generate_blog_post())


if __name__ == "__main__":
    _run_demo()
