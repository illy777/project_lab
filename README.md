# PyEIT Framework with GUI

This project provides a framework with a graphical user interface for working with the PyEIT package. It's meant to be
used with the modifications of the PyEIT package at the Technical University of Chemnitz (TUC). 

## Description

The framework provides a registry file, where new meshes can be registered (lung mesh, forearm mesh, ...). The user has
to implement a function, which processes the voltage data and returns the plotting data. Then this function has be
registered with the mesh type in the registry. In the graphical user interface the new implemented mesh type is then
listed and can be selected. 

[!NOTE] 
The application needs to restart, to recognize a new mesh type. 

## Getting Started

1. clone the repo
```commandline
git clone https://github.com/illy777/project_lab
```
Or use your favorite graphical git tool to clone.

2. Install the project dependencies with [poetry](https://python-poetry.org/) (*recommended way*). (you can find how to install poetry 
[here](https://python-poetry.org/docs/#installing-with-pipx))

3. 

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)