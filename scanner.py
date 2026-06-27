import json
import argparse
import os
import sys
import random # Imported temporarily to mock the computer vision scores

def get_user_profile() -> dict:
    """Prompt the user for baseline skincare context that a camera cannot see."""
    print("\n--- Skincare Context Questionnaire ---")
    
    profile = {}
    
    # We only ask for hidden factors now; the camera does the diagnosing
    profile['skin_type'] = input("What is your baseline skin type? (Oily/Dry/Combo/Normal): ").strip().lower()
    profile['sensitivity'] = input("Is your skin sensitive? (y/n): ").strip().lower() == 'y'
    
    return profile

def validate_image_path(path: str) -> bool:
    """Check if the provided image path exists."""
    return os.path.isfile(path)

def analyze_image_mock(image_path: str) -> dict:
    """
    Placeholder for the OpenCV/MediaPipe pipeline. 
    Eventually, this will analyze pixels and return actual metrics.
    """
    print(f"\n[System] Scanning {image_path} for skin conditions...")
    
    # Mocking detection severity scores (0.0 to 1.0) for testing the CLI
    detections = {
        "acne_severity": random.uniform(0.1, 0.9),
        "dryness_level": random.uniform(0.1, 0.9),
        "hyperpigmentation": random.uniform(0.1, 0.9),
        "wrinkle_depth": random.uniform(0.1, 0.9)
    }
    
    return detections

def main():
    parser = argparse.ArgumentParser(description="Terminal Skincare Analyzer CLI")
    parser.add_argument(
        "image_path", 
        type=str, 
        help="Path to the facial image for analysis (e.g., ./images/face.jpg)"
    )
    
    args = parser.parse_args()

    if not validate_image_path(args.image_path):
        print(f"Error: Could not find image at '{args.image_path}'. Please check the path.", file=sys.stderr)
        sys.exit(1)

    # 1. Gather hidden context from the terminal
    user_profile = get_user_profile()

    # 2. Run the automated image scan (mocked for now)
    scan_results = analyze_image_mock(args.image_path)

    # 3. Display the raw data before the recommendation engine processes it
    print("\n--- Final Analysis Summary ---")
    print(f"User Baseline: {user_profile}")
    print("\nDetected Conditions (Severity Scores 0.0 - 1.0):")
    
    for condition, score in scan_results.items():
        # Format the keys to look clean in the terminal
        formatted_name = condition.replace('_', ' ').title()
        print(f" - {formatted_name}: {score:.2f}")
        
    print("\nSystem ready. Next step: Map these scores to product recommendations.")

if __name__ == "__main__":
    main()
