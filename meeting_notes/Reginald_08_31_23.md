# Reginald 31/08/23

## Notes
- Rosie been working with using llama-index with LLama2 (currently running locally with use of [llama-cpp](https://github.com/abetlen/llama-cpp-python))
    - Went through Rosie's development notebook
- Also had a play around with llama-index chat engine
    - Went through some examples
    - With the chat engine, the model will try to determine if it should query the database (i.e. construct a prompt with some text from the database) or should it just send something to the LLM
        - Can we investigate more about _how_ it does this?
- Is it possible to obtain the prompt to the LLM
    - We know that llama-index does some prompt engineering, but would it be possible to look at that?
    - Also in cases when it tries to refine the answer - does it actually give much benefit?
- Yi-Ling has been looking at llama-index and ideas of how to evaluate the models to see if it's using the knowledge base effectively
    - We should compile some "model" question and answer pairs that we hope our model to get right
    - Start to think about being able to systematically compare models and approaches
- Discussion about documentation
    - Start uploading meeting notes
    - Start documenting the models we try and our experiences with them

## Actions
- Continue with chat engine hacking
    - There are several chat engine choices given by llama-index
        - Compare different approaches and figure out what is the most appropriate
        - Try to figure out when the model is querying and when it is
        - Try to figure out how it makes the decision of whether or not to just have a conversation or not
        - How does this work with small context lengths?
            - How is it remembering/tracking conversation history?
- Maybe start working on Azure rather than local
    - Could be able to run a larger model
    - Might not need GPU if only inference and only for dev
    - Maybe GPU long term?
- Admin:
    - Start meeting note uploads (Ryan)
    - Start model documentation (all)
    - Start project board (Rosie, Levan)
