# languages/

This directory contains nix snippets for various languages such as python, node, lisp, and so on.
Every module need to contain metadata with following structure
```
/*
METADATA_BLOCK_START
{
  "author": "name of the author",
  "description": "Descriptions for module",
  "inputs": {
    "inputs required for module": {
      "attr1": "value",
      "attr2": false
      # ...and so on
    }
  },
  "moduleArgs": {
    "args for module": "corresponding input field's key"
  }
}
METADATA_BLOCK_END
*/
```