import readline
from typing import Final

from reginald.models.base import ResponseModel
from reginald.models.setup_llm import setup_llm

INPUT_PROMPT: Final[str] = ">>> "
REGINALD_PROMPT: Final[str] = "Reginald: "

ART: Final[
    str
] = r"""
(`-') (`-')  _          _    <-. (`-')_(`-')  _        _(`-')
<-.(OO ) ( OO).-/   .->   (_)      \( OO) (OO ).-/   <-. ( (OO ).->
,------,(,------.,---(`-'),-(`-',--./ ,--// ,---.  ,--. ) \    .'_
|   /`. '|  .---'  .-(OO )| ( OO|   \ |  || \ /`.\ |  (`-''`'-..__)
|  |_.' (|  '--.|  | .-, \|  |  |  . '|  |'-'|_.' ||  |OO |  |  ' |
|  .   .'|  .--'|  | '.(_(|  |_/|  |\    (|  .-.  (|  '__ |  |  / :
|  |\  \ |  `---|  '-'  | |  |'-|  | \   ||  | |  ||     ||  '-'  /
`--' '--'`------'`-----'  `--'  `--'  `--'`--' `--'`-----'`------'
"""


def run_chat_interact(streaming: bool = False, **kwargs) -> ResponseModel:
    # set up response model
    response_model = setup_llm(**kwargs)
    user_id = "command_line_chat"
    print(ART)

    while True:
        message = input(INPUT_PROMPT)
        if message in ["exit", "exit()", "quit()", "bye Reginald"]:
            return response_model
        if message == "":
            continue
        if message in ["clear_history", r"\clear_history"]:
            if (
                response_model.mode == "chat"
                and response_model.chat_engine.get(user_id) is not None
            ):
                response_model.chat_engine[user_id].reset()
                print("\n{REGINALD_PROMPT}History cleared.")
            else:
                print("\n{REGINALD_PROMPT}No history to clear.")
            continue

        if streaming:
            response = response_model.stream_message(message=message, user_id=user_id)
            print("")
        else:
            response = response_model.direct_message(message=message, user_id=user_id)
            print(f"\n{REGINALD_PROMPT}{response.message}")
