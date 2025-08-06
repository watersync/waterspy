"""Fields for pydantic models."""
from typing import List, Optional
from pydantic import BeforeValidator
from typing_extensions import Annotated
from waterspy.core.validators import handle_if_below_detection_limit

AnalysisResult = Annotated[float, BeforeValidator(
    handle_if_below_detection_limit)]
