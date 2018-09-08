#!/usr/bin/env python
# ------------------------------------------------------------------------ 79->
# Author: ${name=Kelcey Damage}
# Python: 3.5+
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Doc
# ------------------------------------------------------------------------ 79->
# Dependancies:
#

# Imports
# ------------------------------------------------------------------------ 79->
import hashlib
import uuid
import cbor

# Globals
# ------------------------------------------------------------------------ 79->

# Classes
# ------------------------------------------------------------------------ 79->


class Tools(object):
    """
    NAME:           Tools

    DESCRIPTION:    A class of utility functions used by the datatypes.

    METHODS:        .serialize(obj)
                    Converts an object into a bytes encoded serialized object.

                    .deserialize(obj)
                    Converts a bytes encoded serialized object back into an
                    object.

                    .create_header(meta)
                    Creates a bytes encoded hash(md5) of the metadata.

                    .create_id()
                    Creates a bytes encoded UUID4.
    """
    @staticmethod
    def serialize(obj):
        return cbor.dumps(obj)

    @staticmethod
    def deserialize(obj):
        return cbor.loads(obj)

    @staticmethod
    def create_header(obj):
        return hashlib.md5(cbor.dumps(obj)).hexdigest().encode()

    @staticmethod
    def create_key(obj):
        return hashlib.sha256(cbor.dumps(obj)).hexdigest()

    @staticmethod
    def create_id():
        return str(uuid.uuid4())


# Functions
# ------------------------------------------------------------------------ 79->

# Main
# ------------------------------------------------------------------------ 79->
