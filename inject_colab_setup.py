import os
import json

# The code cell you want to insert at the top of every notebook
SETUP_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {
        "collapsed": False
    },
    "outputs": [],
    "source": [
        "import sys\n",
        "if 'google.colab' in sys.modules:\n",
        "    !uv pip install --system --pre ngsolve"
    ]
}

def inject_setup_to_notebooks(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ipynb'):
                file_path = os.path.join(subdir, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        notebook = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON: {file_path}")
                        continue
                
                # Check if the notebook has cells and if the setup cell is already there
                if 'cells' in notebook and notebook['cells']:
                    first_cell_source = "".join(notebook['cells'][0].get('source', []))
                    
                    if "google.colab" in first_cell_source:
                        print(f"Already present in: {file}")
                        continue
                    
                    # Insert the setup cell at index 0
                    notebook['cells'].insert(0, SETUP_CELL)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(notebook, f, indent=1, ensure_ascii=False)
                    print(f"Successfully injected into: {file}")

# Run the function on your current directory
inject_setup_to_notebooks('.')
