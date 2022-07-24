from typing import List

from dsutil.pipeline.write import PipelineWriter
from dsutil.pipeline.monitor import ReportArtifact


class CSVDatasetWriter(PipelineWriter):
    def write(self, artifacts: List[ReportArtifact]) -> None:
        for artifact in artifacts:
            artifact.data.to_csv(artifact.filename, index=False)
