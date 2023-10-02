# Reginald 02/10/23

## Notes
- Rosie summary of what we've done in the FM
    - Got Llama-2 model running (with `llama-cpp-python` to run quantised versions)
    - Implemented chat engine which can remember chat history instead of a query engine
    - Implemented queue - add stuff to a (asyncio) queue and process queries once at a time
        - You get a clock emoji to say that it's been registered but not yet been processed - this gets changes to a llama when it is being processed
        - Idea for future work to tell you the position in the queue if possible (using the various clock emojis as a count down)
    - Using readers from `llama-hub` to obtain data from different sources
        - Used to have all documents (from wikis, handbooks, turing website, a few Turing courses) inside the repo, but now able to remove the data - just need a `GITHUB_TOKEN` environment variable
        - Can only access Hut23 (in `all_data` index) if you're invited to the repo
    - Almost finished implementing API for machine hosting LLM and the machine hosting the bot
        - Ryan to pick this up and try finish
    - Made several PRs to `llama-index` and `llama-hub` repos
    - Updated README
    - Updated Dockerfiles in the repo
- Remaining tasks to do:
    - Pulumi scripts
    - Testing the splitting of the model and the bot (API) properly
        - It's all been on a local machine at the moment
        - Once we have that, we might be able to actually host the llama-cpp model properly and make it available for some light testing within REG
    - Need to update the blob storage indexes
    - Tech talk to update progress and maybe try to get people to join the project
- Future work
    - Turing slack?
        - Get feedback on team and try get people from REG to help out with specific engineering problems
    - Improve chat history management - can get errors after filling up the context. There is a temprorary fix to clear history using a slack command
    - Evaluation and comparison of models

## Actions
- Rosie to message Turing IT
- Ryan wrap up API stuff
- Get tech talk time in maybe end of November
- Get monthly date in the calendar for Reginald catch up and 22 days work

