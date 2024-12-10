# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from copy import deepcopy
import datetime
import pytest
from ... import types
from .. import pytest_helper


_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI = types._CreateCachedContentParameters(
    model='gemini-1.5-pro-002',
    contents=[
        types.Content(
            role='user',
            parts=[
                types.Part(
                    fileData=types.FileData(
                        fileUri='gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf',
                        mimeType='application/pdf',
                    )
                ),
                types.Part(
                    fileData=types.FileData(
                        fileUri='gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf',
                        mimeType='application/pdf',
                    )
                ),
            ],
        )
    ],
    config={
        'display_name': 'test cache',
        'system_instruction': 'What is the sum of the two pdfs?',
        'ttl': '86400s',
    },
)

_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE = types._CreateCachedContentParameters(
    model='gemini-1.5-pro-001',
    contents=[
        types.Content(
            role='user',
            parts=[
                types.Part(
                    fileData=types.FileData(
                        mimeType='video/mp4',
                        fileUri='https://generativelanguage.googleapis.com/v1beta/files/tjvltve756aa',
                    )
                )
            ],
        )
    ],
    config={
        'display_name': 'test cache',
        'system_instruction': 'What is the sum of the two pdfs?',
        'ttl': '86400s',
    },
)

_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_1 = deepcopy(
    _CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI
)
_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_1.model = (
    'models/gemini-1.5-pro-002'
)
_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_2 = deepcopy(
    _CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI
)
_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_2.model = (
    'publishers/google/models/gemini-1.5-pro-002'
)

_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_PARTIAL_MODEL_1 = deepcopy(
    _CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE
)
_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_PARTIAL_MODEL_1.model = (
    'models/gemini-1.5-pro-001'
)


_EXPIRE_TIME = datetime.datetime.fromisoformat('2024-12-20T00:00:00Z')
_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_EXPIRE_TIME = deepcopy(
    _CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI
)
_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_EXPIRE_TIME.config = {
    'display_name': 'test cache',
    'system_instruction': 'What is the sum of the two pdfs?',
    'expire_time': _EXPIRE_TIME,
}

_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_EXPIRE_TIME = deepcopy(
    _CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE
)
_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_EXPIRE_TIME.config = {
    'display_name': 'test cache',
    'system_instruction': 'What is the sum of the two pdfs?',
    'expire_time': _EXPIRE_TIME,
}


# Replay mode is not supported for caches tests due to the error message
# inconsistency in api and replay mode.
# To run api mode tests, use the following steps:
# 1. First create the resource.
#   sh run_tests.sh pytest -s tests/caches/test_create.py --mode=api
#   1.1 If mldev test_create fails, update the uploaded file using this colab
#       https://colab.sandbox.google.com/drive/1Fv6KGSs0cg6tlpcUHdsclHussXMEGOXk#scrollTo=RSKmFPx00MVL.
# 2. Find the resource name in debugging print and change the resource name constants.py.
# 3. Run and record get and update tests.
#   sh run_tests.sh pytest -s tests/caches/test_get.py --mode=api && sh run_tests.sh pytest -s tests/caches/test_update.py --mode=api && sh run_tests.sh pytest -s tests/caches/test_delete.py --mode=api
test_table: list[pytest_helper.TestTableItem] = [
    pytest_helper.TestTableItem(
        name='test_caches_create_with_gcs_uri',
        exception_if_mldev='INVALID_ARGUMENT',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI,
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_with_gcs_uri_expire_time',
        exception_if_mldev='INVALID_ARGUMENT',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_EXPIRE_TIME,
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_model_partial_path_1',
        exception_if_mldev='INVALID_ARGUMENT',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_1,
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_model_partial_path_2',
        exception_if_mldev='404',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GCS_URI_PARTIAL_MODEL_2,
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_with_googleai_file',
        exception_if_vertex='Internal',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE,
        skip_in_api_mode='Create is not reproducible in the API mode.',
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_with_googleai_file_expire_time',
        exception_if_vertex='Internal',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_EXPIRE_TIME,
        skip_in_api_mode='Create is not reproducible in the API mode.',
    ),
    pytest_helper.TestTableItem(
        name='test_caches_create_with_googleai_file_model_partial_path_1',
        exception_if_vertex='Internal',
        parameters=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE_PARTIAL_MODEL_1,
        skip_in_api_mode='Create is not reproducible in the API mode.',
    ),
]
pytestmark = [
    pytest_helper.setup(
        file=__file__,
        globals_for_file=globals(),
        test_method='caches.create',
        test_table=test_table,
    ),
]
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_async_googleai_file_create(client):
  if client._api_client.vertexai:
    with pytest.raises(Exception):
      await client.aio.caches.create(
          model=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.model,
          contents=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.contents,
          config=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.config,
      )
  else:
    await client.aio.caches.create(
        model=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.model,
        contents=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.contents,
        config=_CREATE_CACHED_CONTENT_PARAMETERS_GOOGLEAI_FILE.config,
    )
