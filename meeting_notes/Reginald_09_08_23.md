# Reginald 08/09/23

## Notes
- Ryan and Rosie almost finishing a PR contribution to llama-index for the following issue: https://github.com/jerryjliu/llama_index/issues/7596
    - ReAct engine seems to be a bit broken after this due to the default system prompt
        - Potentially can make another issue and PR to fix
- Other potential llama-index contributions
    - Some llama-cpp chat engine example notebooks - there's not many (if at all) that exist in the repo and they're very welcome to more examples
    - Ryan to try fix old issue posted during Hackweek (https://github.com/jerryjliu/llama_index/issues/6465)
- Rosie been working on getting GitHub issues and files from within our Hut23
    - Will need to think about what is the personal token that we should use
        - Maybe look at if there's an instituitional token that exists
    - Will need to upload this to Azure as a secret
- Idea: look into logging how good the answers are and save into a database
    - For future, we can maybe use this with a RLHF fine-tuning of our LLM

## Actions
- Ryan & Rosie: look at putting this azure
    - Figure out how to have multiple chat instances at the same time
    - Can start with running the bot locally
- Rosie to think about using the reader for pure markdown files so no need to process them to csv
    - Alternatively, to figure out how the csv files were created from pure markdown files
    - Maybe it was from Andy's scripts to pull data from wiki and handbook
- Ryan to see if we can update the OpenAI code and compare with Llama2
- Ryan & Rosie: Try to get a quantized Llama2-70b running (for Tomas)
- Merge Rosie's current PRs at some point next week
