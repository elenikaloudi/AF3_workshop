#!/bin/bash
#SBATCH --job-name=P31996_with_Q9CR48
#SBATCH --partition=gpu-short
#SBATCH --mem=32GB
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --constraint=A100.4g.40gb|A100.3g.40gb
#SBATCH --cpus-per-task=8
#SBATCH --time=03:30:00
#SBATCH --output="P31996_with_Q9CR48_%j.log"
#SBATCH --error="P31996_with_Q9CR48_%j.err"
#SBATCH --mail-user=e.kaloudi@umail.leidenuniv.nl
#SBATCH --mail-type=BEGIN,END,FAIL


echo "#### Running on nodelogin01"

echo "#### Loading module"
module load alphafold/cc8_3-20250304

echo "#### Checking GPU"
nvidia-smi

echo "#### Running alphafold"

export AF3_RESOURCES_DIR=/data1/databases/AlphaFold3_resources
export AF3_INPUT_DIR=/home/s4178858/data1/alphafold/AFSJson/dram2_test/P31996_with_Q9CR48/
export AF3_OUTPUT_DIR=/home/s4178858/data1/alphafold/output_dram2_test/P31996_with_Q9CR48
export AF3_MODEL_PARAMETERS_DIR=${AF3_RESOURCES_DIR}/weights
export AF3_DATABASES_DIR=${AF3_RESOURCES_DIR}/databases

alphafold \
        --db_dir=${AF3_DATABASES_DIR} \
        --model_dir=${AF3_MODEL_PARAMETERS_DIR} \
        --input_dir=${AF3_INPUT_DIR} \
        --output_dir=${AF3_OUTPUT_DIR}

echo "#### Finished"
