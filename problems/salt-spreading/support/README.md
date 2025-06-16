<!--
SPDX-FileCopyrightText: 2024 Marco Chiarandini <marco@imada.sdu.dk>

SPDX-License-Identifier: CC-BY-4.0
-->

# Tools

## Instance `json` schema

The file `schema.json` can be used to validate the `json` code of the instance
file. For example, using
[check-jsonschema](https://github.com/python-jsonschema/check-jsonschema):

```bash
check-jsonschema --schemafile provaschema.json prova.json -v  
```

## Validator

Usage example:

```bash
python3 src/main.py data/gualandi/gualandi.json -s data/gualandi/gualandi_ransol.json 
```

See `-h` for more.
