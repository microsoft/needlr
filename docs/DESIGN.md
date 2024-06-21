### Package Organization and Structure
For package organization I recommend: 
- docs
- needler
- - admin 
- - core  
- - - workspace 
- - - sourcecontrol 
- - - deploymentpipeline
- - - ...
- - engineering
- - - lakehouse
- - - notebook
- - - environment
- - - ...
- - datascience
- - - model
- - - experiement
- - 
- - item/Artifact ( lakehouse | notebook | environment , ....) 
- samples
- tests 
- utils 
- - semanticModelIOptimization 

Decision to follow API docs for top level imported objects

### Documentation Standard
As a Starting point, we will use Sphinx to document our code.

### Testing Framework
We will use [Pytest](https://docs.pytest.org/en/stable/contents.html#). Pytest fixtures could be used to leverage the same "data" (Workspace) across multiple testing without having to recreate the Workspace on each test

### JSON vs Models
We will use Models to represent the different components of the Needler. We can use [Pydantic](https://docs.pydantic.dev/latest/) to marshal those nasty JSON responses into proper models that will help users of our SDK, add validations when needed, and type safety on assignments. 

### Pagination and Sync calls

- On V0.1. All calls are synchronous.
- Pagination is managed  by call on V0.1. We'll use Generator on subsequent versions
- Throtles - handling retry logic on V.01. 

### Branching Strategy 

- Use main for v0.1
- Use feature branches for new features.
 
### Caching
- No chaching on v0.1
- We will use a simple in-memory cache foror [cachetools](https://cachetools.readthedocs.io/en/stable/) for after v0.1.