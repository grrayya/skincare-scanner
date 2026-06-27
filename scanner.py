import json
import argparse
import os
import sys
import random 

def generate_recommendations(scan_results: dict, database_path: str = "products.json") -> list:
    """Compare scan scores against product thresholds to generate a routine."""
    routine = []
    
    try:
        with open(database_path, 'r') as file:
            database = json.load(file)
            
        for condition, score in scan_results.items():
            # Check if the condition exists in our DB and if the severity beats the threshold
            if condition in database and score >= database[condition]["threshold"]:
                routine.extend(database[condition]["recommendations"])
                
        # Remove duplicates in case multiple conditions trigger the same product
        return list(set(routine))
        
    except FileNotFoundError:
        print(f"\n[!] Note: Could not find '{database_path}'. Skipping product recommendations.")
        return []
        
def get_user_profile() -> dict:
    """Prompt the user for baseline skincare context that a camera cannot see."""
    print("\n✨ Let's get to know your skin a bit better ✨")
    
    profile = {}
    
    # We only ask for hidden factors now; the camera does the diagnosing
    profile['skin_type'] = input("How would you describe your skin naturally? (Oily/Dry/Combo/Normal): ").strip().capitalize()
    profile['sensitivity'] = input("Does your skin tend to be sensitive or easily irritated? (y/n): ").strip().lower() == 'y'
    
    return profile

def validate_image_path(path: str) -> bool:
    """Check if the provided image path exists."""
    return os.path.isfile(path)

def analyze_image_mock(image_path: str) -> dict:
    """
    Placeholder for the OpenCV/MediaPipe pipeline. 
    Eventually, this will analyze pixels and return actual metrics.
    """
    print(f"\n🔍 Scanning your image ({image_path})...")
    
    # Mocking detection severity scores (0.0 to 1.0)
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
    print("\n--- 📋 Scan Results ---")
    
    for condition, score in scan_results.items():
        formatted_name = condition.replace('_', ' ').title()
        
        # Humanize the raw 0.0-1.0 float into a readable intensity level
        if score > 0.7:
            intensity = "High"
        elif score > 0.4:
            intensity = "Moderate"
        else:
            intensity = "Low"
            
        print(f" • {formatted_name}: {intensity} ({int(score * 100)}%)")

    # 4. Generate and display the routine
    routine = generate_recommendations(scan_results)
    
    print("\n--- 🧴 Recommended Action Plan ---")
    if routine:
        print("Based on your scan, we suggest adding these to your routine:")
        for product in routine:
            print(f" [+] {product}")
        print("\nRemember: Introduce new products slowly to protect your skin barrier!")
    else:
        print("Your skin looks well-balanced! Stick to a gentle cleanser and a daily sunscreen.")

if __name__ == "__main__":
    main()
