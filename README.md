# SDMX Experts Workshop Advanced Capacity-building in Amsterdam 

--------

## Setting Up Your Python Coding Environment
[Using Git with Visual Studio Code (Official Beginner Tutoria)](https://www.youtube.com/watch?v=i_23KUAEtUM&ab_channel=VisualStudioCode)

## Overview
Recent changes in best practices for using Python have led to a shift from Anaconda to Visual Studio Code (VS Code) for Jupyter notebooks. This guide will help you set up your coding environment for a seamless experience during our workshop.

## Why These Steps Are Necessary
1. **Better Virtual Environment Management**: VS Code offers superior virtual environment management compared to Anaconda.
2. **Free Access**: Anaconda is now only free for individuals and small organizations, making VS Code a more accessible option.
3. **Integrated Development**: VS Code integrates well with Git and other tools, providing a comprehensive development environment.

## Steps to Set Up Your Coding Environment
This is of course just a recommendation, we don't want anyone to feel pressured to change their trust configuration. But if you want to replicate what you'll see in **Module 2**, here's how to do it.

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
  python -m venv .venv
  ```
  This will create a virtual environment named `.venv`.

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
  
### 7. .gitignore
To ensure that unsafe or unnecessary content is not committed to your repository, make sure to include a `.gitignore` file.

- **Unsafe content**: This includes sensitive information such as API keys and passwords. These should never be committed to your repository.
- **Unnecessary content**: This includes files and directories generated by your development environment, such as virtual environment packages. These should be installed using the `requirements.txt` file.

A basic `.gitignore` file might look like this:
    ```bash
    # Ignore all hidden files and directories
    .*
    ```


## Advanced: Managing Python Versions with pyenv
For those who need to work with multiple Python versions, pyenv is a powerful tool that allows you to easily switch between versions on a per-project basis. Here's how to set it up:

### Setup Guide
#### macOS and Linux

1. Install pyenv:
```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash
```

2. Add to your shell configuration file (.bashrc, .zshrc, etc.):
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

3. Restart your shell or run source ~/.bashrc (or equivalent).

#### Windows

1. Install pyenv-win:
```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

2. Add System Environment Variables:

 - PYENV: %USERPROFILE%\.pyenv\pyenv-win
 - PYENV_HOME: %USERPROFILE%\.pyenv\pyenv-win
 - Add to PATH: %PYENV%\bin;%PYENV%\shims

3. Restart your terminal.

### Usage (all platforms)

1. Install a Python version:
```bash
Copypyenv install 3.9.0
```

2. Set a global Python version:
```bash
Copypyenv global 3.9.0
```

3. Set a local (project-specific) Python version:
```bash
Copycd your-project
pyenv local 3.9.0
```

4. Verify the active Python version:
```bash
Copypython --version
```

pyenv allows you to manage Python versions efficiently across different projects, ensuring consistency and avoiding conflicts between different Python installations.



## Conclusion
Following these steps will ensure you have a well-configured environment for coding, making it easier to manage dependencies and work on projects efficiently. Happy coding!

Sources:
1. [Running Jupyter notebook in VS Code, set up, getting started with python in VS Code](https://www.youtube.com/watch?v=9V7AoX0TvSM)
2. [How to Install Jupyter Notebook in VSCode | Jupyter Notebook in Visual Studio Code (Easy)](https://www.youtube.com/watch?v=xS5ZXOC4e6A)
3. [Jupyter Notebook Tutorial: Introduction, Setup, and Walkthrough](https://www.youtube.com/watch?v=HW29067qVWk)
4. [Jupyter Notebooks in VS Code - Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
5. [Getting Started with Jupyter Notebooks in VS Code](https://learn.microsoft.com/en-us/shows/visual-studio-code/getting-started-with-jupyter-notebooks-in-vs-code)
6. [How To Setup Python + Jupyter Notebook + VS Code on Windows](https://www.raillyhugo.com/blog/how-to-setup-python-environment)
7. [GitHub - microsoft/vscode-jupyter: VS Code Jupyter extension](https://github.com/microsoft/vscode-jupyter)
8. [Wikipedia/Visual_Studio_Code](https://en.wikipedia.org/wiki/Visual_Studio_Code)