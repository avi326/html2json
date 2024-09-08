import os
import json
from difflib import SequenceMatcher


def compare_dicts(dict1, dict2):
    if dict1 == dict2:
        return 1.0
    similarity = sum(
        SequenceMatcher(None, str(dict1.get(k, '')), str(dict2.get(k, ''))).ratio()
        for k in set(dict1) | set(dict2)
    )
    return similarity / max(len(dict1), len(dict2))


def evaluate_json_pair(true_data, pred_data):
    # Check main structure
    main_parts = ['header', 'body', 'footer']
    structure_check = all(part in true_data and part in pred_data for part in main_parts)

    results = {
        'structure_valid': structure_check,
        'header_similarity': compare_dicts(true_data.get('header', {}), pred_data.get('header', {})),
        'body_content_match': true_data.get('body', {}).get('content') == pred_data.get('body', {}).get('content'),
        'body_headers_similarity': compare_dicts(
            true_data.get('body', {}).get('headers', {}),
            pred_data.get('body', {}).get('headers', {})
        ),
        'footer_similarity': compare_dicts(true_data.get('footer', {}), pred_data.get('footer', {})),
    }

    # Calculate overall match percentage
    results['match_percentage'] = (
                                          (results['header_similarity'] * 0.25) +
                                          (results['body_content_match'] * 0.25) +
                                          (results['body_headers_similarity'] * 0.25) +
                                          (results['footer_similarity'] * 0.25)
                                  ) * 100

    return results


def evaluate_all_files(directory):
    results = []
    true_files = {}
    pred_files = {}

    # Separate true and pred files
    for filename in os.listdir(directory):
        if filename.endswith('_metadata.json'):
            true_files[filename.split('_')[0]] = filename
        elif filename.endswith('_metadata_pred.json'):
            pred_files[filename.split('_')[0]] = filename

    # Evaluate pairs
    for file_id in true_files.keys():
        if file_id in pred_files:
            true_file = os.path.join(directory, true_files[file_id])
            pred_file = os.path.join(directory, pred_files[file_id])

            with open(true_file, 'r') as file:
                true_data = json.load(file)
            with open(pred_file, 'r') as file:
                pred_data = json.load(file)

            evaluation = evaluate_json_pair(true_data, pred_data)
            evaluation['file_name'] = true_files[file_id]
            results.append(evaluation)

    return results


# Usage
directory = "./dataset/train/metadata"
evaluation_results = evaluate_all_files(directory)

# Print individual results
for result in evaluation_results:
    print("=" * 50)
    print(f"File: {result['file_name']}")
    print("=" * 50)
    print(f"Structure valid: {'✓' if result['structure_valid'] else '✗'}")
    print("\nHeader:")
    print(f" Similarity: {result['header_similarity']:.2f}")
    print("\nBody:")
    print(f" Content match: {'✓' if result['body_content_match'] else '✗'}")
    print(f" Headers similarity: {result['body_headers_similarity']:.2f}")
    print("\nFooter:")
    print(f" Similarity: {result['footer_similarity']:.2f}")
    match_percentage = result['match_percentage']
    print("\nOverall Match:")
    print(f" Percentage: {match_percentage:.2f}%")
    print(" Quality: ", end="")
    if match_percentage >= 90:
        print("Excellent 🌟")
    elif match_percentage >= 75:
        print("Good 👍")
    elif match_percentage >= 50:
        print("Fair 😐")
    else:
        print("Poor 😞")
    print("\n" + "-" * 50 + "\n")

# Calculate and print average statistics
valid_results = [result for result in evaluation_results if result['structure_valid']]
if valid_results:
    average_match_percentage = sum(result['match_percentage'] for result in valid_results) / len(valid_results)
    print(f"Average match percentage across all successfully evaluated items: {average_match_percentage:.2f}%")
    print(
        f"Total samples: {len(evaluation_results)}, Successfully evaluated: {len(valid_results)}, Problematic: {len(evaluation_results) - len(valid_results)}")
else:
    print("No valid results to calculate statistics.")