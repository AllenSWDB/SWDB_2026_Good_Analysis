""" top level run script """
import subprocess
import os
from pathlib import Path

def run():
    code_dir = Path('/code')

    # All notebooks to execute
    notebooks = [
        'solutions/Workshop2_solutions.ipynb',
        'solutions/Workshop2-extended_solutions.ipynb',
        'mini-workshops/nb1/mini-workshop-1_solutions.ipynb',
        'mini-workshops/nb2/mini-workshop-2_solutions.ipynb',
        'mini-workshops/nb3/mini-workshop-3_solutions.ipynb',
        'mini-workshops/nb4/mini-workshop-4_solutions.ipynb',
    ]

    for nb in notebooks:
        nb_path = code_dir / nb
        subprocess.run([
            'jupyter', 'nbconvert', '--to', 'notebook',
            '--execute', '--inplace',
            f'--ExecutePreprocessor.kernel_cwd={nb_path.parent}',
            str(nb_path)
        ], check=True)

if __name__ == "__main__":
    run()