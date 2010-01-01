# Tst Library

This library provides a framework for writing Python-based tests (often, but not necessarily, for testing Python libraries) that emit a transcript of results for verification against an authoritative version.

Interface documentation can be directly found in the library file, [libraries/tst.py](../libraries/tst.py), in Javadoc-esque documentation comments.

## Licence

The content of the Tst repository is free software; you can redistribute it and/or modify it under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl-2.0.txt) as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

The content is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

## Quick Start

*   Ensure that the contents of [libraries](../libraries) is available on PYTHONPATH e.g. `export PYTHONPATH=/path/to/Tst/libraries:${PYTHONPATH}`.
*   Run the tests by running the runtsts.py utility from the working directory (or archive) root (Tst's tests are written using Tst).
