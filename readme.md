# HTML Table Parsing and Metadata Generation: Comprehensive Technical Report

## 1. Project Overview

This project focuses on parsing HTML tables and generating corresponding metadata JSON files using two distinct approaches:
1. A rule-based method
2. A fine-tuned Language Model (LLM) method using Microsoft's Phi-3 model

The goal is to create a robust, adaptable system capable of handling various table structures while considering execution time and computational costs.

## 2. Problem Statement

The core challenge involves parsing code-generated HTML tables from diverse files and producing metadata JSON files comprising three main sections: Header, Body, and Footer. The solution must be:
- Adaptable to changes in table structures
- Scalable for future retraining
- Optimized for execution time and computational costs

## 3. Approach 1: Rule-Based Method

### 3.1 Methodology
The rule-based approach relies on predefined patterns in HTML table structures, assuming consistent patterns across input files.

### 3.2 Key Features
- Utilizes BeautifulSoup library for HTML parsing
- Employs regular expressions for extracting specific elements (e.g., table IDs)
- Implements custom rules to identify and divide content into header, body, and footer sections

### 3.3 Advantages
- Extremely fast execution due to minimal computational overhead
- No requirement for training data or fine-tuning
- Highly interpretable and easily updatable

### 3.4 Limitations
- May struggle with variable or unconventional table structures
- Requires manual adjustments for new table patterns

### 3.5 Performance Results
- **Test Set**: 111 samples
- **Success Rate**: 99.97%
- **Evaluation Process**: The evaluation checks for element-wise matching in Header, Body, and Footer sections between the generated metadata and the ground truth. This ensures accuracy not just in overall structure, but in the detailed content of each section.

### 3.6 Time and Cost Considerations
- **Execution Time**: Processes HTML tables in seconds, ideal for large-scale, repetitive tasks
- **Cost**: Low, runs efficiently on CPUs without need for expensive GPUs or cloud resources

## 4. Approach 2: Fine-Tuned LLM (Phi-3)

### 4.1 Methodology
This approach employs Microsoft's Phi-3 model, fine-tuned specifically for HTML-to-metadata parsing tasks, enabling more flexible and context-aware understanding of table elements.

### 4.2 Key Features
- Fine-tuned on project-specific data for identifying table components
- Utilizes advanced language modeling techniques for diverse table formats
- Captures nuanced and implicit relationships within table data

### 4.3 Fine-Tuning Process
- Conducted on Google Colab with custom dependencies
- Dataset preprocessed to JSONL format for compatibility with training pipeline

### 4.4 Model Availability
- Fine-tuned version available on Hugging Face: "avi32636/phi-3.5-mini-html2json"
- Accessible for performance checking and further development

### 4.5 Advantages
- High adaptability to diverse table structures
- Strong contextual understanding of table components
- Publicly accessible for replication and improvement

### 4.6 Limitations
- Slower execution, requiring GPU acceleration
- Higher operational costs due to GPU resource requirements

### 4.7 Performance Results
- **Training Set**: 24,000 examples
- **Test Set:** 100 samples
- **Success Rate**: 100% output generation (no complete failures)
- **Quality Issues**: 10% of outputs had JSON syntax errors, requiring re-processing
- **Evaluation Process**: Similar to the rule-based method, the evaluation involves element-wise comparison in Header, Body, and Footer sections between the LLM-generated metadata and the ground truth. This rigorous checking ensures high fidelity in the parsed output across all table components.

### 4.8 Time and Cost Considerations
- **Execution Time**: Several seconds per table on GPU, significantly slower than rule-based method
- **Cost**: High, requires cloud resources or dedicated hardware for large-scale use

## 5. Installation and Usage

### 5.1 Rule-Based Method
1. Install required libraries: `pip install beautifulsoup4`
2. Run `main.py` script to process the HTML files and generate metadata
3. After running `main.py`, execute `eval.py` to evaluate the results and get performance metrics
   - The `eval.py` script performs a detailed comparison between the generated metadata and the ground truth, checking for element-wise matching in Header, Body, and Footer sections
   - This evaluation provides a comprehensive assessment of the parsing accuracy, ensuring that each component of the table structure is correctly captured

### 5.2 Fine-Tuned LLM Method
1. Use `files2jsonl_phi3.5.py` to convert HTML files to JSONL format for fine-tuning
2. Train model using scripts in `Phi_3_finetuning_for_html2json.ipynb` notebook
3. For inference, use the Hugging Face model "avi32636/phi-3.5-mini-html2json"

## 6. Performance Comparison

### 6.1 Accuracy
- **Rule-Based**: 99.97% success rate on 111 test files, with element-wise matching in Header, Body, and Footer sections
- **LLM-Based**: 100% output generation, 10% require re-processing due to JSON syntax errors. Evaluation includes detailed element matching across all table sections

### 6.2 Speed
- **Rule-Based**: Very fast, minimal processing requirements
- **LLM-Based**: Slower, requires GPU acceleration for real-time results

### 6.3 Cost
- **Rule-Based**: Low-cost, runs on CPUs
- **LLM-Based**: Higher cost, requires GPUs

### 6.4 Adaptability
- **Rule-Based**: Requires manual updates for new patterns
- **LLM-Based**: Generalizes to unseen structures, dependent on training data quality
