import logging
import os
from time import sleep
from typing import Any, Callable, Final, Iterable

from rich.progress import Progress, SpinnerColumn, TextColumn

REGINAL_PROMPT: Final[str] = "Reginald: "


def stream_progress_wrapper(
    streamer: Callable | Iterable,
    task_str: str = REGINAL_PROMPT,
    progress_bar: bool = True,
    end: str = "\n",
    *args,
    **kwargs,
) -> Any:
    """Add a progress bar for iteration.

    Examples
    --------
    >>> from time import sleep
    >>> def sleeper() -> str:
    ...    sleep(1)
    ...    return 'hi'
    >>> stream_progress_wrapper(streamer=sleeper)
    <BLANKLINE>
    Reginald:
    'hi'
    >>> stream_progress_wrapper(streamer=sleeper, progress_bar=False)
    Reginald:
    'hi'
    """
    if isinstance(streamer, Callable):
        streamer = streamer(*args, **kwargs)
    if progress_bar:
        with Progress(
            TextColumn("{task.description}[progress.description]"),
            SpinnerColumn(),
            transient=True,
        ) as progress:
            progress.add_task(task_str)
    print(task_str, end=end)
    return streamer


def get_env_var(
    var: str, log: bool = True, secret_value: bool = True, default: str = None
) -> str | None:
    """
    Get environment variable. Logs provided if log is True.

    Parameters
    ----------
    var : str
        Name of environment variable
    log : bool, optional
        Whether or not to log if reading was successful, by default True
    secret_value : bool, optional
        Whether or not the value is a secret, by default True.
        If True, the value will not be logged.
        Ignored if log is False.
    default : str, optional
        Default value if environment variable is not found, by default None

    Returns
    -------
    str | None
        Value of environment variable, or None if not found
    """
    if log:
        logging.info(f"Trying to get environment variable '{var}'")
    value = os.getenv(var, default=default)

    if log:
        if value is not None:
            if secret_value:
                logging.info(f"Got environment variable '{var}' successfully")
            else:
                logging.info(f"Got environment variable '{var}' successfully: {value}")
        else:
            logging.warn(f"Environment variable '{var}' not found.")

    return value
