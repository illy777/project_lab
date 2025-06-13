## How to use the framework

To integrate a new mesh into the framework follow these steps. (An example can be seen in ```circular_mesh.py```)

1. Create a new python file named after your new mesh type in the ```pipelines``` directory.

2. Three new classes have to be created for the new mesh type. One for the mesh, one for the model and one for the
pipeline. These have to inherit respectively from the templates ```Mesh```, ```Model``` and ```Pipeline``` in
```app/factory.py```.

3. The mesh class has to implement the method ```generate_mesh()```. This method needs to return the mesh object.

4. The model class has to implement the ```load_model(model_name: str, model_file: str, load_function: callable)```
method. The method needs to load a given model from a given file path by using the given load_function.

5. The pipeline class has to implement the ```evaluate_data(data: np.ndarray) -> np.ndarray``` method. This method takes
the voltages from electrodes as input and returns the processed mesh data. In this class the desired pipeline needs to
be implemented.

6. Create a choose function for the new mesh type in the ```PipelineRegistry``` class in the ```pipelines/registry.py```
file. This function needs to return an instance of the pipeline class for that mesh type. E.g.
```CircularMeshPipeline``` for the circular mesh.

7. Finally add the new mesh type with the choose function to the dictionary ```_meshoptions``` in the
```pipelines/registry.py``` file. E.g. ```"myFancyMesh": self._choose_my_fancy_mesh```.
