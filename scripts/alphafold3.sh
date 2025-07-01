#!/bin/bash
#SBATCH --job-name=
#SBATCH --partition=gpu-short
#SBATCH --mem=42GB
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --constraint=A100.4g.40gb|A100.3g.40gb
#SBATCH --cpus-per-task=8
#SBATCH --time=04:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --mail-user=
#SBATCH --mail-type=BEGIN,END,FAIL

echo "#### Running on $(hostname)"

echo "#### Loading module"
module load alphafold/cc7_3-20250304

echo "#### Checking GPU"
nvidia-smi

echo "#### Running alphafold"

export AF3_RESOURCES_DIR=/data1/databases/AlphaFold3_resources
export AF3_INPUT_DIR=
export AF3_OUTPUT_DIR=
export AF3_MODEL_PARAMETERS_DIR=${AF3_RESOURCES_DIR}/weights
export AF3_DATABASES_DIR=${AF3_RESOURCES_DIR}/databases

alphafold \
        --db_dir=${AF3_DATABASES_DIR} \
        --model_dir=${AF3_MODEL_PARAMETERS_DIR} \
        --input_dir=${AF3_INPUT_DIR} \
        --output_dir=${AF3_OUTPUT_DIR}

echo "#### Finished"
