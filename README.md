Rejuvenome Redun 06
---

## Self-serve registration 

```
python3 -m pip install --upgrade latch
# Ensure docker is running.
latch register wf-rejuvenome-nf_redun_06 # From directory above root
```

## Quick Start on Latch Console

Upload your test data and a sample CSV to the platform.

```
# From the repository root

latch cp fc1.csv latch:///fs1.csv
latch cp nf-redun-06/test/sample1/expt_FC1_L4_1.fastq.gz latch:///expt_FC1_L4_1.fastq.gz
latch cp nf-redun-06/test/sample1/expt_FC1_L4_2.fastq.gz latch:///expt_FC1_L4_2.fastq.gz
# etc.
```

Use the "Import CSV" button to populate batched workflows using the `fc1.csv`
file.
