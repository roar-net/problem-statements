# Tools

## Instance `json` schema

The file `schema.json` can be used to validate the `json` code of the instance
file. For example, using
[check-jsonschema](https://github.com/python-jsonschema/check-jsonschema):

```bash
check-jsonschema --schemafile provaschema.json prova.json -v  
```
