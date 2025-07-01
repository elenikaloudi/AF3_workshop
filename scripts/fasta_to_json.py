#!/usr/bin/env python3
import os
import random
import json
import argparse
from Bio import SeqIO


def parse_fasta_file(fasta_file: str):
    """
    Parse a FASTA file and extract sequences.
    
    Args:
        fasta_file: Path to the FASTA file.
    
    Returns:
        List of parsed sequences.
    """
    with open(fasta_file, "r") as file:
        return list(SeqIO.parse(file, "fasta"))


def create_json_structure_single(protein, num_seeds):
    """
    Convert sequence data to the required JSON structure for a single protein.
    
    Args:
        protein: The protein sequence.
        num_seeds: Number of random model seeds.
    
    Returns:
        JSON dictionary for a single protein JSON file.
    """
    model_seeds = [random.randint(1, 30000) for _ in range(num_seeds)]
    
    return {
        "name": protein.id,
        "dialect": "alphafoldserver",
        "version": 1,
        "modelSeeds": model_seeds,
        "sequences": [
            {
                "proteinChain": {
                    "sequence": str(protein.seq),
                    "count": 1
                }
            }
        ]
    }


def create_json_structure_ppi(bait, prey, num_seeds):
    """
    Convert sequence data to the required JSON structure for PPI (bait-prey interaction).

    Args:
        bait: The bait protein sequence.
        prey: The prey protein sequence.
        num_seeds: Number of random model seeds.
    
    Returns:
        JSON dictionary for a PPI JSON file.
    """
    model_seeds = [random.randint(1, 30000) for _ in range(num_seeds)]

    return {
        "name": f"{bait.id}_with_{prey.id}",
        "dialect": "alphafoldserver",
        "version": 1,
        "modelSeeds": model_seeds,
        "sequences": [
            {
                "proteinChain": {
                    "sequence": str(bait.seq),
                    "count": 1
                }
                },
                {
                "proteinChain": {
                    "sequence": str(prey.seq),
                    "count": 1
                }
            }
        ]
    }


def process_fasta_files(bait_file, prey_dir, num_seeds):
    """
    Process either a bait protein and a directory of prey proteins or single proteins
    in the directory to generate JSON files.

    Args:
        bait_file: Path to the bait protein FASTA file (can be None for single proteins).
        prey_dir: Directory path to the FASTA files of prey proteins or single proteins.
        num_seeds: Number of random model seeds.
    """
    # Case 1: Bait-Prey Interaction (PPI)
    if bait_file:
        # Parse the bait protein
        bait_sequences = parse_fasta_file(bait_file)
        if len(bait_sequences) != 1:
            print("Error: The bait FASTA file should contain exactly one protein sequence.")
            return

        bait = bait_sequences[0]

        # Process each prey protein in the directory
        for file in os.listdir(prey_dir):
            if file.endswith(".fasta") or file.endswith(".fa"):
                prey_file = os.path.join(prey_dir, file)
                prey_sequences = parse_fasta_file(prey_file)
                
                for prey in prey_sequences:
                    # Generate the JSON structure for the bait-prey interaction
                    json_data = create_json_structure_ppi(bait, prey, num_seeds)
                    
                    # Write to the output JSON file
                    output_filename = f"{os.path.splitext(file)[0]}_with_{bait.id}.json"
                    with open(output_filename, "w") as json_file:
                        json.dump([json_data], json_file, indent=4)
                    print(f"Processed {prey_file} -> {output_filename}")
    
    # Case 2: Single Proteins in the Directory (No Bait-Prey Interaction)
    else:
        # Process each protein in the directory
        for file in os.listdir(prey_dir):
            if file.endswith(".fasta") or file.endswith(".fa"):
                prey_file = os.path.join(prey_dir, file)
                prey_sequences = parse_fasta_file(prey_file)
                
                for prey in prey_sequences:
                    # Generate the JSON structure for the single protein
                    json_data = create_json_structure_single(prey, num_seeds)
                    
                    # Write to the output JSON file
                    output_filename = f"{os.path.splitext(file)[0]}.json"
                    with open(output_filename, "w") as json_file:
                        json.dump([json_data], json_file, indent=4)
                    print(f"Processed {prey_file} -> {output_filename}")


def main():
    parser = argparse.ArgumentParser(description="Convert FASTA sequences to AlphaFold3 JSON format.")
    parser.add_argument("prey_dir", help="Directory containing the FASTA files of prey proteins.")
    parser.add_argument("--bait", help="Path to the FASTA file containing the bait protein.")
    parser.add_argument("--seeds", type=int, default=20, help="Number of random seeds to generate (default: 20).")
    
    args = parser.parse_args()

    process_fasta_files(args.bait, args.prey_dir, args.seeds)


if __name__ == "__main__":
    main()

