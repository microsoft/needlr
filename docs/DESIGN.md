### Package Organization and Structure
For package organization I recommend: 
- docs
- needler 
- - core 
- - - admin 
- - - workspace 
- - - sourcecontrol 
- - - deploymentpipeline
- - - ...
- - item/Artifact ( lakehouse | notebook | environment , ....) 
- samples
- tests 
- utils 
- - semanticModelIOptimization 

### Documentation Standard
As a Starting point, we will use Sphinx to document our code.

### Testing Framework
We will use [Pytest](https://docs.pytest.org/en/stable/contents.html#). Pytest fixtures could be used to leverage the same "data" (Workspace) across multiple testing without having to recreate the Workspace on each test

### JSON vs Models
We will use Models to represent the different components of the Needler. We can use [Pydantic](https://docs.pydantic.dev/latest/) to marshal those nasty JSON responses into proper models that will help users of our SDK, add validations when needed, and type safety on assignments. 
