# Biosystems project

## Goal
 Design a program which extracts biochemical networks from kegg database
 and find an optimal path from molecule A to molecule B 
 
 See [KEGG](https://kegg.jp) (Kyoto Encyclopedia of Genes and Genomes)
 
## Design
 1. Extraction - KEGG rest api
 2. Organization
 3. Path Identification - depth-first search algorithm
 4. Optimization
 
## Dependencies
 - python >3.0
 - urllib3; for info: see [Repo here](https://github.com/urllib3/urllib3)
 - certifi; to install: `pip install certify`
 - requests; to install: `pip install requests`

## How to use
 - run `python cli.py` and enter `help` in prompt

## License
