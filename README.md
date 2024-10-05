# sdmx-workshop
SDMX Experts Workshop Advanced Capacity-building in Amsterdam 

TODO:
1. Solve importing the api key for the participants and not showing mine
    - in the chat_bot the api key should be imported in the app once and passed to the llm as well as the embedding
2. SDMX parsing should be done using the sdmx1 lib (mapping is the main question to filter codes and resolve their names)

----------

# Setting Up Your Python Coding Environment

## Overview
Recent changes in best practices for using Python have led to a shift from Anaconda to Visual Studio Code (VS Code) for Jupyter notebooks. This guide will help you set up your coding environment for a seamless experience during our workshop.

## Why These Steps Are Necessary
1. **Better Virtual Environment Management**: VS Code offers superior virtual environment management compared to Anaconda.
2. **Free Access**: Anaconda is now only free for individuals and small organizations, making VS Code a more accessible option.
3. **Integrated Development**: VS Code integrates well with Git and other tools, providing a comprehensive development environment.

## Steps to Set Up Your Environment

### 1. Install Python, Git, and Visual Studio Code
- **Python**: Download and install the latest version from the [official Python website](https://www.python.org/downloads/).
- **Git**: Download and install Git from the [official Git website](https://git-scm.com/downloads).
- **Visual Studio Code**: Download and install VS Code from the [official VS Code website](https://code.visualstudio.com/).

### 2. Install the Jupyter Notebook Extension in VS Code
- Open VS Code.
- Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window.
- Search for "Jupyter" and install the Jupyter extension.

### 3. Clone the Workshop Repository
- Open a terminal in VS Code.
- Navigate to the folder where you want to download the workshop contents.
- Run the following command to clone the repository:
  ```bash
  git clone <repository-url>
  ```
  Replace `<repository-url>` with the URL of the workshop repository.

### 4. Create a Virtual Environment
- In the terminal, navigate to the cloned repository folder.
- Run the following command to create a virtual environment:
  ```bash
  python -m venv env
  ```
  This will create a virtual environment named `env`.

### 5. Activate the Virtual Environment
- **Windows**:
  ```bash
  .\env\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source env/bin/activate
  ```

### 6. Install Required Libraries
- Ensure you are in the virtual environment.
- Run the following command to install the required libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Conclusion
Following these steps will ensure you have a well-configured environment for coding, making it easier to manage dependencies and work on projects efficiently. Happy coding!

Source: Conversation with Copilot, 05/10/2024
(1) Running Jupyter notebook in VS Code, set up, getting started with python in VS Code. https://www.youtube.com/watch?v=9V7AoX0TvSM.
(2) How to Install Jupyter Notebook in VSCode | Jupyter Notebook in Visual Studio Code (Easy). https://www.youtube.com/watch?v=xS5ZXOC4e6A.
(3) Jupyter Notebook Tutorial: Introduction, Setup, and Walkthrough. https://www.youtube.com/watch?v=HW29067qVWk.
(4) Jupyter Notebooks in VS Code - Visual Studio Code. https://code.visualstudio.com/docs/datascience/jupyter-notebooks.
(5) Getting Started with Jupyter Notebooks in VS Code. https://learn.microsoft.com/en-us/shows/visual-studio-code/getting-started-with-jupyter-notebooks-in-vs-code.
(6) How To Setup Python + Jupyter Notebook + VS Code on Windows. https://www.raillyhugo.com/blog/how-to-setup-python-environment.
(7) GitHub - microsoft/vscode-jupyter: VS Code Jupyter extension. https://github.com/microsoft/vscode-jupyter.
(8) en.wikipedia.org. https://en.wikipedia.org/wiki/Visual_Studio_Code.