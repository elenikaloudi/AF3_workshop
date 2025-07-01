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
	- Q9DC58
	- O70404
	- Q9CZX7
	- Q6GSS7
	- P61161
	- C0HKE1
	- P31996
	- P17047
	- Q99KI0
	- Q9QY73
	- Q8R143
	- Q922T2
	- Q5SRX1
	- Q91YT8
	- Q91VK4
	- O88384


• Q9DC58      • O70404      • Q9CZX7      • Q6GSS7      • P61161      • C0HKE1 

• P31996      • P17047      • Q99KI0      • Q9QY73      • Q8R143      • Q922T2

• Q5SRX1      • Q91YT8      • Q91VK4      • O88384   



### The input page on AlphaFoldServer should look like that:

![AlphafoldServer input](assets/alphafoldserver.png)


---

## 🙌 Thanks for Participating!

We hope this workshop gives you the confidence to explore and predict protein interactions.

## Happy folding! 🧬
