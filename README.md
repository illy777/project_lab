# PyEIT Framework with GUI

This project provides a framework with a graphical user interface for working with the PyEIT package. It's meant to be
used with the modifications of the PyEIT package at the Technical University of Chemnitz (TUC). 

## Description

The framework provides a registry file, where new meshes can be registered (lung mesh, forearm mesh, ...). The user has
to implement a function, which processes the voltage data and returns the plotting data. Then this function has be
registered with the mesh type in the registry. In the graphical user interface the new implemented mesh type is then
listed and can be selected. 

> [!NOTE] 
> The application needs to restart, to recognize a new mesh type. 

## Getting Started

**clone the repo**
```commandline
git clone https://github.com/illy777/project_lab
```
Or use your favorite graphical git tool to clone.

### Install dependencies with poetry (recommended way)

1. First you have to install [poetry](https://python-poetry.org/). (you can find the instructions 
[here](https://python-poetry.org/docs/#installing-with-pipx))

2. If you're using Pycharm you can add a local interpreter and create a new environment. As shown in the image below you
need to select poetry as the type. Furthermore, you have to select the right python version and if poetry is installed
the path to the poetry executable should be selected automatically.

<img src="Docs/add_python_interpreter_poetry.PNG" alt="drawing" width="400">

> [!TIP]
> You can find the python version of the project in the pyproject.toml file.

3. After creation of the poetry environment pycharm should install als dependencies automatically from the 
pyproject.toml file.

4. If you want to use poetry from the console just change to the project root directory and type the following command.

````commandline
poetry install
````

### Install dependencies manually (not recommended way)

You could install all the dependencies manually with pip. The dependencies are listed in the pyproject.toml file.
At least you should use a virtual environment for better control of conflicting packages. If things don't work that way
try to install the dependencies the recommended way [above](#install-dependencies-with-poetry-recommended-way).

### Running the project

To start the program you need to run the *main.py* script in the root directory of the project. If you are using poetry
you can use the following to run the program, when you are in the root directory of the project:

````commandline
poetry run python .\main.py
````

Otherwise, you can set up a run-configuration in pycharm or your favorite IDE to run the main.py file. If you've setup
the poetry environment pycharm should use it automatically to run python.

## Dependencies

- All dependencies are listed in pyproject.toml
- The project focuses on running on windows, but linux or mac should also work.

## Development

If you want to further develop the project you should use poetry for dependency management. You can find detailed
instructions on how to use poetry [here](https://python-poetry.org/docs/basic-usage/). 

Quick overview (terminal):

- Adding new dependencies:
````commandline
poetry add <package-name>(optional verion restrictions)
````

- To 'save' your dependence setup you have to lock it into the *poetry.lock* file. This can be done as following:
````commandline
poetry lock
````

> [!TIP]
> You should commit the poetry.lock file into git. Because these locked dependencies are used for installation and makes
> your setup reproducible.

## Authors

- Isaac Lucas de Lima Yuki <[isaacyuki@hotmail.com](mailto:isaacyuki@hotmail.com)>
- Ömer Faruk KANMAZ <[kanmazomerfaruk@outlook.com](mailto:kanmazomerfaruk@outlook.com)>
- Ivana Kotaras <[kotaras.ivana@gmail.com](mailto:kotaras.ivana@gmail.com)>
- Thomas Harald Reinhard Rubin <[thomas.rubin2@protonmail.com](mailto:thomas.rubin2@protonmail.com)>

## License

This project is licensed under the MIT License - see the LICENSE.md file for details