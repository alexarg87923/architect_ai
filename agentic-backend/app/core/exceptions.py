from fastapi import HTTPException

class ProjectSpecificationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class RoadmapGenerationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class NodeExpansionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class NodeEditError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)