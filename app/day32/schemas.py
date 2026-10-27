from pydantic import BaseModel, Field


class StoryAnalysis(BaseModel):
    business_goal: str

    missing_requirements: list[str]

    implementation_steps: list[str]

    story_points: int = Field(ge=1, le=13)