import readline
from typing import Final

from reginald.models.base import ResponseModel
from reginald.models.setup_llm import setup_llm

from ..utils import REGINALD_PROMPT

INPUT_PROMPT: Final[str] = ">>> "
EXIT_STRS: set[str] = {"exit", "exit()", "quit()", "bye Reginald"}
CLEAR_HISTORY_STRS: set[str] = {"clear_history", r"\clear_history"}

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
        if message in EXIT_STRS:
            return response_model
        if message == "":
            continue
        if message in ["clear_history", r"\clear_history"]:
            if (
                response_model.mode == "chat"
                and response_model.chat_engine.get(user_id) is not None
            ):
                response_model.chat_engine[user_id].reset()
                print(f"\n{REGINALD_PROMPT}History cleared.")
            else:
                print(f"\n{REGINALD_PROMPT}No history to clear.")
            continue

        if streaming:
            response = response_model.stream_message(message=message, user_id=user_id)
            print("")
        else:
            response = response_model.direct_message(message=message, user_id=user_id)
            print(f"\n{REGINALD_PROMPT}{response.message}")
