# Reginald 15/09/23

## Notes
- Updates on recent llama-index contributions
    - Our PR has been merged into llama-index: https://github.com/jerryjliu/llama_index/pull/7597#issuecomment-1712010196
    - Some other contributions to llama-index over this last week
        - PR for fixing an issue that came up during hackweek was merged into llama-index: https://github.com/jerryjliu/llama_index/pull/7607
        - A PR to llama-index for updating their llama-cpp example in docs: https://github.com/jerryjliu/llama_index/pull/7616
        - A PR to fix a bug introduced to LlamaCPP: https://github.com/jerryjliu/llama_index/pull/7650
    - More llama-index contributions?
        - We could maybe contribute some end-to-end examples to the repo too
- Updates on Reginald (Rosie, Ryan)
    - Updated our hackweek code for implementing the query engine
        - Previous code had some old classes in llama-index which are depreciating in the future
    - Llama-2 CPP added to the available models
    - Ddded chat engine functionality to slack bot
    - Been running things locally, so need to update the bot that is running on Azure
        - Maybe we can keep the OpenAI one but make sure that is _only_ using public data
        - Create a new bot which has all private data (along with the GitHub readers that Rosie's been looking at)
- Some current issues
    - Queuing system
        - Currently it's possible to crash it by sending multiple requests while it's still processing the previous
        - Rosie has made good progress on fixing this, but currently it will only emoji and respond to one message. Would be good to emoji immediately on all but queue the queries to the LLM
    - Multiple chat instances
        - Each user to have a chat history
        - Some issues to consider
            - When do we refresh a chat history for a user?
                - Maybe add option for user to acknowledge that their query was answered - manual refresh of history
            - Timer that deletes chat history after a certain time
            - Are there any privacy concerns of us hosting the chat history?
            - How do we queue queries coming from different users?
                - Maybe best to just do it by time they posted that query. Hopefully the responses don't take too long anyway
                - How many users do we actually expect to be using it at the same time?
- Demo for next week
    - Aim to have minimal Llama-2-CPP model running on Azure
        - If not, we can run it locally
        - Will still have the OpenAI running as well
    - Rosie: one idea is to write a notebook example that reads in PDF reports and compare it with just using ChatGPT
    - Do we need slides?

## Actions

- Ryan to message James R to discuss Azure
- Rosie to continuing looking at queuing system
- Rosie and Ryan to continue thinking about how we deal with multiple users of the chat engine
- Focus on making the demo smooth
