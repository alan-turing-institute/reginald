# Scraped data 

Scraped data using code from Andy P (link TODO).

Currently data generation run via pytest, pending development of CLI for tool.

Hacky process I used for now:

(TODOs mostly to link to Andy's code if he's happy to do so, otherwise ask James B or Andy)

```
# clone scraping repo
git clone TODO

# clone data sources
git clone --recurse-submodules https://github.com/alan-turing-institute/REG-handbook.git
git clone https://github.com/alan-turing-institute/research-engineering-group.wiki.git

# build REG handbook
pushd REG-handbook
hugo --minify # requires hugo
popd

# use scraping repo
cd TODO

# edit code to point to local copies
# edit tests/interact_se_connector/test_scrapper.py::test_do_walk
TODO



# venv and install
python -m venv env
source env/bin/activate
pip install -e .
pip install html5

# generate data
# note: will fail but will generate files in tests/interact_se_connector/output 
pytest tests/interact_se_connector/test_scrapper.py::test_do_walk
```

scraped csvs have header:
`,url,id,title,is_public,body,summary,author,keywords`
