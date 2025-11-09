from pydantic import BaseModel, constr, validator

class ProjectSpecification(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: constr(max_length=500)
    goals: list[constr(max_length=200)]
    timeline: constr(max_length=100)

    @validator('goals')
    def validate_goals(cls, goals):
        if not goals:
            raise ValueError('At least one goal must be provided.')
        return goals

class RoadmapNode(BaseModel):
    id: int
    title: constr(min_length=1, max_length=100)
    description: constr(max_length=500)
    dependencies: list[int] = []

    @validator('dependencies', pre=True)
    def validate_dependencies(cls, dependencies):
        if dependencies is None:
            return []
        return dependencies

class Roadmap(BaseModel):
    title: constr(min_length=1, max_length=100)
    nodes: list[RoadmapNode]

    @validator('nodes')
    def validate_nodes(cls, nodes):
        if not nodes:
            raise ValueError('At least one node must be included in the roadmap.')
        return nodes

def validate_project_specification(spec: ProjectSpecification):
    return spec.dict()

def validate_roadmap(roadmap: Roadmap):
    return roadmap.dict()