# Security Requirements Analysis Pipeline

## Team Members
- **Dylan Walker** (Email: dbw0034@auburn.edu)
- **Josh Daniels** (Email: jsd0045@auburn.edu)

## Model Used for Task 1
For the Extractor phase (Task 1), we are utilizing the **Google Gemma-3-1B-it** (`google/gemma-3-1b-it`) model. 

*Note on Implementation Details:* Because the input security documents are over 100 pages long, no local 1B parameter model can read the entire document at once without exhausting its context window or hardware memory constraints. To solve this, **we implemented chunking/sampling in Task 1** to process the documents in manageable chunks, ensuring the model can accurately extract Key Data Elements (KDEs) without crashing or hallucinating.

## Project Structure
We have carefully organized the repository for clarity:
- `src/`: Contains all of the main task logic (`main_task1.py`, `main_task2.py`, `main_task3.py`, `demo.py`, etc.).
- `outputs/`: This is where all generated output files will be saved during execution.
- `data/`: Contains the input PDFs.
- `dist/`: Contains the PyInstaller compiled standalone executable.
- `test_scripts/`: Contains the individual test bash scripts (hidden away to prevent clutter).

## How to Run the Pipeline (For TAs / Graders)
To make grading as simple as possible, we have provided a single entry point script at the root of the repository.

You **do not** need to install any Python dependencies or use the virtual environment, as the entire application has been compiled into a standalone binary using PyInstaller.

To run the pipeline with a given combination of documents, simply execute the `run.sh` bash script and provide the two input PDF files:

```bash
./run.sh --doc1 data/cis-r1.pdf --doc2 data/cis-r2.pdf
```

### What to Expect:
1. **Phase 1 (Extractor):** The script will load the PDFs, extract KDEs using Gemma-3-1B, and save the results as `.yaml` files in the `outputs/` folder. Prompts and logs will be saved to `outputs/PROMPT.md` and `outputs/llm_outputs.txt`.
2. **Phase 2 (Comparator):** The script will compare the elements and requirements between the two generated `.yaml` files, producing `.txt` differences in the `outputs/` folder.
3. **Phase 3 (Executor):** The script will map differences to Kubescape controls and output a final scan result CSV named `scan_results_<name>.csv` in the `outputs/` folder.

All generated data stays perfectly contained within the `outputs/` directory.
