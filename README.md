# PyEIT Framework with GUI

This project provides a framework with a graphical user interface for working with the PyEIT package.
It's meant to be used with the modifications of the PyEIT package at the Technical University of
Chemnitz (TUC).

## Description

The framework provides a registry file where new meshes can be registered (lung mesh, forearm mesh,
etc.). The user has to implement a function that processes the voltage data and returns the plotting
data. Then this function has to be registered with the mesh type in the registry. In the graphical user
interface, the newly implemented mesh type is listed and can be selected.

> [!NOTE]
> The application needs to restart to recognize a new mesh type.

## Getting Started

Clone this repo:

```commandline
git clone https://github.com/illy777/project_lab
```

### Install dependencies with poetry

1. Install [poetry](https://python-poetry.org/) (you can find the instructions
   [here](https://python-poetry.org/docs/#installing-with-pipx)).

2. If PyCharm is used, a new virtual environment needs to be created and added as the interpreter. As
   shown in the image below, poetry needs to be selected as the type. Furthermore, the correct Python
   version has to be selected. The path to the poetry executable should be selected automatically.

    <img src="Docs/add_python_interpreter_poetry.PNG" alt="drawing" width="400">


3. After creation of the poetry environment, PyCharm should install all dependencies automatically from
   the [pyproject.toml](pyproject.toml) file.

To install the dependencies from the console, the following command can be used:

```commandline
poetry install
```

> [!TIP]
> To configure the virtual environment inside the project folder, use: `poetry config virtualenvs.in-project true`

> [!TIP]
> The Python version of the project can be found in the [pyproject.toml](pyproject.toml) file.

### Install dependencies manually

The dependencies from the [pyproject.toml](pyproject.toml) file can also be installed manually with pip.
Then the packages will be installed manually on the host machine, and the installed package versions
might be uninstalled to install the required ones.

```commandline
pip install -r requirements.txt
```

### Running the project

To start the program, the *main.py* script needs to be run in the root directory of the project. If
poetry is used, the following command can be used to run the script:

```commandline
poetry run python main.py
```

Otherwise, a run configuration has to be set up in PyCharm or any other IDE to run the main.py file. If
you've set up the poetry environment, PyCharm should use it automatically to run Python.

## Dependencies

* All dependencies are listed in [pyproject.toml](pyproject.toml)
* The project focuses on running on Windows, but Linux or macOS should also work.

## Development

To add a new mesh type to the framework, follow the instructions
[here](pipelines/README.md).

The project is divided into three parts: backend, frontend, and pipelines. The following table gives an
overview of how these are structured.

| Part    | Folder | Description                                                                                        |
| ------- | ------ | -------------------------------------------------------------------------------------------------- |
| Backend | app    | Contains the backend thread, which fetches the voltage data, hands it over to the chosen pipeline and sends the result to the GUI for visualisation.|
| Frontend      | gui       | Contains the GUI classes for the frontend thread to display all widgets.                         |
| Pipelines     | pipelines | Contains all classes and files for the mesh types needed to use the framework.                   |

Detailed instructions on how to use poetry can be found
[here](https://python-poetry.org/docs/basic-usage/).

Quick overview (terminal):

* Adding new dependencies:

```commandline
poetry add <package-name>  # optional version restrictions
```

* The dependency setup of the project is saved in the `poetry.lock` file. This can be done as follows:

```commandline
poetry lock
```

> [!TIP]
> The poetry.lock file can be committed into Git because these locked dependencies are used for
> installation and make the setup reproducible.

## Authors

* Isaac Lucas de Lima Yuki <[isaacyuki@hotmail.com](mailto:isaacyuki@hotmail.com)>
* Ömer Faruk KANMAZ <[kanmazomerfaruk@outlook.com](mailto:kanmazomerfaruk@outlook.com)>
* Ivana Kotaras <[kotaras.ivana@gmail.com](mailto:kotaras.ivana@gmail.com)>
* Thomas Harald Reinhard Rubin <[thomas.rubin2@protonmail.com](mailto:thomas.rubin2@protonmail.com)>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
