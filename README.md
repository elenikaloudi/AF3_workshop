# 🧬 Welcome to the AlphaFold Workshop: 
# Protein-Protein Interaction Predictions

Hello and welcome! 👋  

This repository is part of a hands-on workshop on using `AlphaFold` to predict **protein-protein interactions**. In this guide, you'll learn how to:

- Collect protein sequences
- Prepare them for multimer predictions
- Run AlphaFold on the server and on the HPC
- Analyze the results and structure quality

Whether you're a beginner in structural biology or just trying to automate your protein interaction screening, this walkthrough is for you!

---

# 🧪 What We'll Do in This Workshop

In this workshop, we will focus on predicting interactions between a protein of interest and a list of candidate partners using structure-based modeling.

The goal is to predict how each candidate might interact directly with the protein of interest. To do this, we’ll combine their sequences into pairs, generate 3D models and assess whether a meaningful interaction is likely.

**By the end of the session, you'll understand how to:**

- Go from UniProt IDs to structural models 

- Prepare sequence pairs for interaction prediction

- Evaluate the predicted structures to identify high-confidence interactions

This approach is useful for generating testable hypotheses about protein binding, interaction networks, and functional partnerships.




## 🚀 Step 1: Get Your Protein Sequences

To predict protein-protein interactions using AlphaFold, we need to provide both protein sequences. Each protein is represented by its amino acid sequence (in FASTA format). Below you can find the UniProt IDs for the Target protein and the partner proteins we are going to test. Feel free to choose one (or more) partner protein.

You can get protein sequences from [UniProt](https://www.uniprot.org/)


- **Target protein:**

	- Dram2_mouse (Q9CR48) 


- **Partner proteins:**

	* Q9DC58
	* O70404	     
	* Q9CZX7
	* Q6GSS7
	* P61161	   
	* C0HKE1 
	* P31996    
	* P17047
	* Q99KI0
	* Q9QY73
	* Q8R143
	* Q922T2
	* Q5SRX1
	* Q91YT8
	* Q91VK4
	* O88384   




## :facepunch: Step 2: Running a protein-protein prediction on AlphaFoldServer


You need to Login to the [AlphaFoldServer](https://alphafoldserver.com/) page online. If you do not have an account, you can quickly create one. :bowtie:


## The input page on AlphaFoldServer should look like that:

![AlphafoldServer input](assets/alphafoldserver.png)




### To do:

1. Copy the target protein **Fasta** and paste it in the **input box**

2. Select **'Add entity'** to add another input box

3. Copy and paste the partner protein **Fasta** in the other **input box**

4. Select **'Continue and preview this job'**

5. Give a **name** to your job (recommended: Protein IDs)

6. Select **'Confirm and submit this job'**


**Notes:**

* It takes 2-3 min to run a protein-protein prediction, depending on the size of the proteins, so take a sip of coffee!

* You probably have a lot of questions about your model (at least I did the first time). 

* Let's try to assess the output together. What do you think about your model?

![AlphaFoldServer - Dram1 dimer](assets/dram1_dimer.png) 


## :wrench: Step 3: Installing some tools

Before we proceed with folding proteins on the Cluster, we have some tools to install. I hope this will not take long!


### Tool 1: MobaXterm

MobaXterm is a powerful SSH client and terminal with X11 server support. Here's how to get it:

**Steps:**

1. Go to the official website: [MobaXterm](200~https://mobaxterm.mobatek.net/download.html)

2. Choose the version:

	- Download the Home Edition.

	- Choose the Installer edition (so it installs like a normal program) or Portable edition (just unzip and run).

3. Install (if you chose Installer edition):

	- Run the .exe file.

	- Follow the installation steps.

4. Use the instructions on [ALICE WIKI](https://pubappslu.atlassian.net/wiki/spaces/HPCWIKI/pages/37519361/ALICE)

### Tool 2: Pymol

PyMOL is a molecular visualization system. You can install the open-source version or the commercial one.


#### - Option A: Install Open-Source PyMOL (via Conda)

**Requirements:**

	Install Anaconda or Miniconda


**Steps (in Anaconda Prompt):**

```
conda create -n pymol-env -c schrodinger pymol
conda activate pymol-env
pymol
```

This creates a new environment and installs PyMOL from the Schrödinger channel.


#### - Option B: Commercial Pymol

1. Follow the link: [Pymol](https://www.pymol.org/)

2. Sign up or purchase a license. 

	You can also use my licence: :speak_no_evil:

	Download the [license](assets/pymol-edu-license.lic)

3. Download the installer for your OS and follow the instructions.



## :bomb: Step 4.1: Creating the input for running AlphaFold on the HPC 

You are now at the step of preparing input files to run interaction modeling on an HPC cluster using AlphaFold3.

To run interaction modeling on the cluster, we need to prepare inputs that define which two proteins should be modeled together as a complex. The input should be Json files. This format makes it easy to automate many pairwise runs between a protein of interest and multiple partners.

**To Do:**

1. Upload the `FASTA` sequences on your directory 

2. Convert to `.json` 

	Convert your `Fasta` to `json` by running the [script](scripts/fasta_to_json.py)

Convert as Bait–Prey Interactions

```
python fasta_to_json.py path/to/input/directory --bait path/to/bait.fasta
```

**Notes:**

`bait.fasta` should contain exactly one protein sequence.

Output files will be named like: `PreyProtein_with_BAIT.json`.

Random model seeds are automatically generated (default = 20). You can change this with --seeds:
`python fasta_to_json.py ... --seeds 50`



3. Move all your `json` files in a directory

	To create a directory:

```
mkdir name_of_directory
```

4. To move all the `json` files at once run:


```
mv *.json /path/to/the/directory
```


## :star: Step 4.2: Organize JSON Files into Subdirectories

After generating `JSON` files, you can organize each into its own folder using the [script](scripts/organize_json.sh).

The output directory of the previous step will be the input directory for this step. So, make sure that all the json files are in one directory.


**What it does:**

For every `*.json` file in the provided directory:

- Creates a new subdirectory named after the file.

- Moves the file into its corresponding directory.


## 🚀 Step 5: Submitting Jobs to the HPC Cluster

Once your JSON input files are ready, you can launch the interaction prediction jobs by submitting them to the cluster.

Each job will:

- Read one JSON file (defining the protein pair)

- Run AlphaFold3

- Save the predicted complex and confidence scores

You can use the [script](scripts/master_script.sh) 


This script goes through each folder inside a main directory. For every folder, it creates a SLURM job script, sets the correct input and output paths, and submits the job to the cluster using `sbatch`.

**Usage**

Each subdirectory must contain a valid AlphaFold3 input `.json` file.

Input directory structure:

`master_dir/
├── job1/
│ └── input.json
├── job2/
│ └── input.json
`

You first need to set the environmental paths as stated above and then run:

```
bash master_script.sh /path/to/master_dir
```


#### **Don't forget:**

The script needs some adjustments before submitting it!

**Note:**

It needs about 1h to run, so let's not waste time and get the output from the [output folder](output_dram2_test)


## :mag_right: Step 6: Filter high confidence interactions

After generating predicted complexes, we can filter out low-confidence interactions by analyzing the Predicted Aligned Error (PAE) scores between chains.

PAE provides a per-residue estimate of how well the model predicts the relative position of two regions — in our case, the two protein chains. Lower PAE values at the interface indicate a more confident prediction of the interaction.

**PAE extraction:**

This script processes AlphaFold or similar model outputs by reading `summary_confidences.json` files to extract between-chain Predicted Aligned Error (PAE) statistics. It filters results based on an optional PAE threshold and outputs a CSV file summarizing the results.


You can find the script [here](scripts/pae_filtered_10.py).


The script extracts average, min, and max between-chain PAE values from structured model output directories.


**Usage:**

Run the script by editing the last line by specifying the `input_dir`, `output_dir` and the `pae_threashold`.

```
python pae_filtered_10.py
```

### Notes:

This will:

- Traverse the directory tree to locate all`*summary_confidences.json` files.

- Extract between-chain PAE values.

- Write output rows to a CSV file containing:

        - Directory

        - Average PAE

        - Minimum PAE

        - Maximum PAE

        - All extracted PAE values (comma-separated)

- Skips any `.json` that doesn't contain `chain_pair_pae_min`.


#### Tips:

Prepare Input Directory

The input should be a master directory structured like this:

```
input_directory/
├── protein_1/
│   └── model_1/
│       └── result_summary_confidences.json
├── protein_2/
│   └── model_1/
│       └── result_summary_confidences.jsonn
...

```

Each `.json` file should contain a `"chain_pair_pae_min"` matrix.


##  :art: Step 7: Visualization

Once the interaction predictions are complete, you can explore the resulting protein complexes in PyMOL to examine structural details and binding interfaces.

The `output` directory you have contains many files. The one you are intrested in for visualization, the structure, is the `.cif` file. Click on that and open it in your computer.

#### Feel free to explore Pymol


---

## 🙌 Thanks for Participating!

We hope this workshop gives you the confidence to explore and predict protein interactions.

If you have questions or you want to contact me, send me an email: elenikaloudi1@gmail.com

## Happy folding! 🧬
