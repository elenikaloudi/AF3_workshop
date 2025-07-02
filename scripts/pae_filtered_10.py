import os
import json
import csv
import glob
import statistics

def extract_pae_stats(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        pae_matrix = data.get("chain_pair_pae_min", [])
        n = len(pae_matrix)

        # Extract off-diagonal (between-chain) PAE values
        between_chain_values = [
            pae_matrix[i][j]
            for i in range(n)
            for j in range(n)
            if i != j
        ]

        if not between_chain_values:
            return None

        return {
            "avg": sum(between_chain_values) / len(between_chain_values),
            "min": min(between_chain_values),
            "max": max(between_chain_values),
            "all_values": between_chain_values
        }

    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return None

def main(master_dir, output_csv, pae_threshold=None):
    output_rows = []

    protein_dirs = sorted(os.listdir(master_dir))

    for protein_dir in protein_dirs:
        protein_path = os.path.join(master_dir, protein_dir)
        if not os.path.isdir(protein_path):
            continue

        subdirs = [d for d in os.listdir(protein_path) if os.path.isdir(os.path.join(protein_path, d))]
        for subdir in subdirs:
            subdir_path = os.path.join(protein_path, subdir)
            json_candidates = glob.glob(os.path.join(subdir_path, "*summary_confidences.json"))

            for json_path in json_candidates:
                stats = extract_pae_stats(json_path)
                if stats is None:
                    print(f"⚠️ No usable chain_pair_pae_min in {json_path}")
                    continue

                if pae_threshold is None or stats["avg"] <= pae_threshold:
                    flat_values = ", ".join([f"{v:.2f}" for v in stats["all_values"]])
                    output_rows.append([
                        protein_dir,
                        f"{stats['avg']:.2f}",
                        f"{stats['min']:.2f}",
                        f"{stats['max']:.2f}",
                        flat_values
                    ])
                    print(f"✅ Processed {json_path} (avg PAE: {stats['avg']:.2f})")
                else:
                    print(f"⏭️ Skipped {json_path} (avg PAE {stats['avg']:.2f} > threshold {pae_threshold})")

    if output_rows:
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Directory", "Avg_Between_Chain_PAE", "Min", "Max", "All_Values"])
            writer.writerows(output_rows)
        print(f"\n✅ Done! Output saved to: {output_csv}")
    else:
        print("🚫 No valid data extracted.")

# Example usage:
main("path/to/input/directory", "path/to/output/directory/.csv", pae_threshold=10)

