#!/bin/bash

# Check if master directory is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 master_dir"
    exit 1
fi

# Master directory
master_dir="$1"

# Check if master directory exists
if [ ! -d "$master_dir" ]; then
    echo "Error: Directory '$master_dir' not found!"
    exit 1
fi

# Loop through each directory inside master_dir
for dir in "$master_dir"/*/; do
    # Remove trailing slash and extract directory name
    dir_name=$(basename "$dir")

    # Define job script file
    job_script="${dir}/batch_${dir_name}.sh"

    # Create the SLURM script in each directory
    cat <<EOL > "$job_script"
#!/bin/bash
#SBATCH --job-name=${dir_name}
#SBATCH --partition=gpu-short
#SBATCH --mem=32GB
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --constraint=A100.4g.40gb|A100.3g.40gb
#SBATCH --cpus-per-task=8
#SBATCH --time=03:30:00
#SBATCH --output="${dir_name}_%j.log"
#SBATCH --error="${dir_name}_%j.err"
#SBATCH --mail-user=
#SBATCH --mail-type=BEGIN,END,FAIL


echo "#### Running on $(hostname)"

echo "#### Loading module"
module load alphafold/cc8_3-20250304

echo "#### Checking GPU"
nvidia-smi

echo "#### Running AlphaFold"

export AF3_RESOURCES_DIR=/data1/databases/AlphaFold3_resources
export AF3_INPUT_DIR=${dir}
export AF3_OUTPUT_DIR=/${dir_name}
export AF3_MODEL_PARAMETERS_DIR=\${AF3_RESOURCES_DIR}/weights
export AF3_DATABASES_DIR=\${AF3_RESOURCES_DIR}/databases

alphafold \\
        --db_dir=\${AF3_DATABASES_DIR} \\
        --model_dir=\${AF3_MODEL_PARAMETERS_DIR} \\
        --input_dir=\${AF3_INPUT_DIR} \\
        --output_dir=\${AF3_OUTPUT_DIR}

echo "#### Finished"
EOL

    # Submit the job
    sbatch "$job_script"

    echo "Submitted job for ${dir_name}"
done

echo "All jobs submitted."
echo "If it folds, it’s biology. If it crashes, it’s your script. Keep calm and trust AlphaFold." 🧪💻
