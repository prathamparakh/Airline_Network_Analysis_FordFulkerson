# Ford-Fulkerson Algorithm for Maximum Flow with BFS

This project implements the Ford-Fulkerson algorithm using Breadth-First Search (BFS) to calculate the maximum flow in a directed graph. The graph is constructed from a dataset of flight networks stored in a CSV file. This README outlines the project's purpose, usage, and setup instructions.

## Features

- **Graph Construction**: Automatically builds a directed graph from a CSV dataset using NetworkX.
- **Ford-Fulkerson Algorithm**: Implements the classic algorithm for computing maximum flow with augmenting paths found via BFS.
- **Path Tracking**: Stores all augmenting paths and their corresponding flow values.
- **CSV Integration**: Reads input datasets and exports results with computed flow values.
- **Data Preprocessing**: Cleans and merges raw datasets to generate the input for the algorithm.

## Requirements

- **Python**: 3.7+
- **Required Libraries**:
  - `pandas`
  - `networkx`

## How to Use
- **Step 1: Prepare the Dataset**
    - Ensure your raw datasets are correctly formatted and placed in the 1_data_cleaning/datasets directory.
    - Run merge_script.py to generate the preprocessed flight_network.csv file.

- **Step 2: Run the Main Script**
    - Navigate to the 3_implementation directory and execute the script to compute the maximum flow between a specified source and sink:

- **Step 3: Review the Results**
    - The maximum flow value will be displayed in the console.
    - The updated dataset with computed flow values will be exported as flight_network_flows.csv. This can be used further for visualizations.

## Customization
To customize the source and sink nodes, edit the following lines in max_flow.py:

```python
src, snk = "BOM", "MAA"
```
Replace BOM and MAA with your desired source and sink node identifiers.
