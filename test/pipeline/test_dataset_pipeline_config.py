import unittest

from dsutil.pipeline import (
    DatasetPipelineConfig,
    PassthroughReader,
)


class DatasetPipelineConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = DatasetPipelineConfig(
            name='config_name',
            reader=PassthroughReader(data=list()),
        )

    def test_uuid(self) -> None:
        config_uuid = self.config.uuid
        self.assertEqual(len(config_uuid), 36)
        self.assertEqual(len(config_uuid.split('-')), 5)
