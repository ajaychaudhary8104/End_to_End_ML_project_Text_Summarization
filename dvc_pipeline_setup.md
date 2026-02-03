# DVC Data Tracking Pipeline Setup

This document describes the DVC (Data Version Control) configuration for the Text Summarization project.

## Overview

DVC is configured to track:
- **Data Artifacts**: Training, validation, and test datasets
- **Models**: Trained model weights and checkpoints
- **Parameters**: Training hyperparameters from `params.yaml`
- **Metrics**: Performance metrics from each pipeline stage

## DVC Configuration Files

### 1. `dvc.yaml` - Pipeline Definition
This file defines the complete ML pipeline with 5 stages:

#### Stage 1: Data Ingestion
- **Command**: Downloads and extracts the SAMSum dataset
- **Outputs**: `artifacts/data_ingestion/samsum_dataset/`
- **Tracked Artifacts**: Raw dataset (cached)

#### Stage 2: Data Validation
- **Command**: Validates that all required files exist in the dataset
- **Inputs**: Ingested dataset
- **Outputs**: Validation status file
- **Tracked Artifacts**: Status file (not cached for visibility)

#### Stage 3: Data Transformation
- **Command**: Tokenizes and prepares data for model training
- **Inputs**: Ingested dataset
- **Outputs**: `artifacts/data_transformation/samsum_dataset/`
- **Tracked Artifacts**: Tokenized dataset (cached)

#### Stage 4: Model Training
- **Command**: Trains the Pegasus model on the prepared data
- **Inputs**: Transformed dataset, training parameters
- **Parameters**: TrainingArguments from `params.yaml`
- **Outputs**: 
  - Trained model: `artifacts/model_trainer/pegasus-samsum-model/`
  - Tokenizer: `artifacts/model_trainer/tokenizer/`
- **Tracked Artifacts**: Model and tokenizer (cached)

#### Stage 5: Model Evaluation
- **Command**: Evaluates the trained model on test data
- **Inputs**: Transformed dataset, trained model, tokenizer
- **Outputs**: `artifacts/model_evaluation/metrics.csv`
- **Tracked Artifacts**: Metrics (not cached)

### 2. `dvc.lock` - Pipeline Lock File
Stores the exact versions and hashes of all pipeline outputs. This ensures reproducibility.

### 3. `.dvcignore` - Ignore Patterns
Specifies files and directories DVC should ignore (similar to `.gitignore`).

## Usage

### Initialize DVC
```bash
dvc init
```

### Run the Pipeline
```bash
# Run all stages
dvc repro

# Run specific stage
dvc repro -s data_ingestion
dvc repro -s model_trainer

# Force re-run without checking dependencies
dvc repro --force
```

### View Pipeline Status
```bash
# Show pipeline DAG
dvc dag

# Show pipeline status
dvc status
```

### Track Remote Storage
```bash
# Add remote storage (e.g., S3, Google Cloud, etc.)
dvc remote add myremote s3://mybucket/path

# Set default remote
dvc remote default myremote

# Push data to remote
dvc push

# Pull data from remote
dvc pull
```

### View Metrics
```bash
# Compare metrics across experiments
dvc metrics diff

# Show current metrics
dvc metrics show
```

### Experiment Tracking
```bash
# Create a new experiment with parameter changes
dvc exp run -S TrainingArguments.num_train_epochs=2

# View experiment results
dvc exp show

# Compare experiments
dvc exp compare
```

## DVC Tracker Utility

The `dvc_tracking.py` module provides a `DVCTracker` class for logging metrics within pipeline stages:

```python
from textSummarizer.pipeline.dvc_tracking import get_dvc_tracker

tracker = get_dvc_tracker()

# Log metrics from a stage
metrics = {
    "accuracy": 0.95,
    "loss": 0.05
}
tracker.log_metrics("model_evaluation", metrics)

# Log data artifacts
tracker.log_data("data_transformation", "artifacts/data_transformation/samsum_dataset")

# Log models
tracker.log_model("model_trainer", "artifacts/model_trainer/pegasus-samsum-model", "transformer")
```

## Directory Structure

```
project/
├── dvc.yaml                          # Pipeline definition
├── dvc.lock                          # Pipeline lock file (auto-generated)
├── .dvc/
│   ├── .gitignore                    # DVC ignore patterns
│   ├── config                        # DVC configuration
│   └── ...
├── artifacts/
│   ├── data_ingestion/
│   │   ├── .metrics.json             # Stage metrics
│   │   └── samsum_dataset/
│   ├── data_validation/
│   │   ├── .metrics.json
│   │   └── status.txt
│   ├── data_transformation/
│   │   ├── .metrics.json
│   │   └── samsum_dataset/
│   ├── model_trainer/
│   │   ├── .metrics.json
│   │   ├── pegasus-samsum-model/
│   │   └── tokenizer/
│   └── model_evaluation/
│       ├── metrics.csv               # Final evaluation metrics
│       └── .metrics.json
└── ...
```

## Best Practices

1. **Regular Commits**: Commit `dvc.lock` to git to ensure reproducibility
2. **Remote Storage**: Set up remote storage for collaboration (S3, GCS, Azure Blob, etc.)
3. **Experiment Tracking**: Use `dvc exp` for hyperparameter tuning
4. **Metrics Visualization**: Use `dvc metrics` to compare results
5. **Data Access**: Keep data in remote storage, pull locally as needed

## Integration with CI/CD

DVC can be integrated with CI/CD pipelines for automated model training and evaluation:

```bash
# In CI/CD pipeline
dvc pull                # Pull latest data
dvc repro              # Run pipeline
dvc push               # Push results to remote
```

## Documentation Links

- [DVC Official Documentation](https://dvc.org/doc)
- [DVC Pipelines](https://dvc.org/doc/user-guide/pipelines)
- [DVC Remote Storage](https://dvc.org/doc/user-guide/data-management/remote)
- [DVC Experiments](https://dvc.org/doc/user-guide/experiment-management)
