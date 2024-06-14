import logging
import os
from itertools import chain
from typing import Any, Callable, Final, Generator, Iterable

from rich.progress import Progress, SpinnerColumn, TextColumn

REGINALD_PROMPT: Final[str] = "Reginald: "


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


def create_folder(folder: str) -> None:
    """
    Function to create a folder if it does not already exist.

    Parameters
    ----------
    folder : str
        Name of the folder to be created.
    """
    if not os.path.exists(folder):
        logging.info(f"Creating folder '{folder}'")
        os.makedirs(folder)
    else:
        logging.info(f"Folder '{folder}' already exists")


def stream_progress_wrapper(
    streamer: Callable,
    task_str: str = REGINALD_PROMPT,
    use_spinner: bool = True,
    end: str = "\n",
    *args,
    **kwargs,
) -> Any:
    """Add a progress bar for iteration.

    Parameters
    ----------
    streamer
        Funciton to add the `SpinnerColumn` while running
    task_str
        What to print whether `use_spinner` is `True` or not,
        and if `use_spinner` is `True` is printed prior to
        the `SpinningColumn`.
    use_spinner
        Whether to print the `SpinnerColumn` or not.
    end
        What to pass to the `end` parameter of `print` calls.
    args
        Any arguments to pass to `streamer`
    kwargs
        Any keyward arguments to pass to `streamer`.

    Examples
    --------
    >>> from time import sleep
    >>> def sleeper(seconds: int = 3) -> str:
    ...     sleep(seconds)
    ...     return f'{seconds} seconds nap'
    >>> stream_progress_wrapper(sleeper)
    <BLANKLINE>
    Reginald:
    '3 seconds nap'
    >>> stream_progress_wrapper(sleeper, use_spinner=False, end='')
    Reginald: '3 seconds nap'
    """
    if use_spinner:
        with Progress(
            TextColumn("{task.description}[progress.description]"),
            SpinnerColumn(),
            transient=True,
        ) as progress:
            progress.add_task(task_str)
            results: Any = streamer(*args, **kwargs)
        print(task_str, end=end)
        return results
    else:
        print(task_str, end=end)
        return streamer(*args, **kwargs)


def stream_iter_progress_wrapper(
    streamer: Iterable | Callable | chain,
    task_str: str = REGINALD_PROMPT,
    use_spinner: bool = True,
    end: str = "",
    *args,
    **kwargs,
) -> Iterable:
    """Add a progress bar for iteration.

    Parameters
    ----------
    streamer
        `Iterable`, `Callable` or `chain` to add the `SpinnerColumn`
        while iteraing over. A `Callabe` will be converted to a
        `Generator`.
    task_str
        What to print whether `use_spinner` is `True` or not,
        and if `use_spinner` is `True` is printed prior to
        the `SpinningColumn`.
    use_spinner
        Whether to print the `SpinnerColumn` or not.
    end
        What to pass to the `end` parameter of `print` calls.
    args
        Any arguments to pass to `streamer`
    kwargs
        Any keyward arguments to pass to `streamer`.

    Examples
    --------
    >>> from time import sleep
    >>> def sleeper(naps: int = 3) -> Generator[str, None, None]:
    ...     for nap in range(naps):
    ...         sleep(1)
    ...         yield f'nap: {nap}'
    >>> tuple(stream_iter_progress_wrapper(streamer=sleeper))
    <BLANKLINE>
    Reginald: ('nap: 0', 'nap: 1', 'nap: 2')
    >>> tuple(stream_iter_progress_wrapper(
    ...     streamer=sleeper, use_spinner=False))
    Reginald: ('nap: 0', 'nap: 1', 'nap: 2')
    """
    if isinstance(streamer, Callable):
        streamer = streamer(*args, **kwargs)
    if use_spinner:
        with Progress(
            TextColumn("{task.description}[progress.description]"),
            SpinnerColumn(),
            transient=True,
        ) as progress:
            if isinstance(streamer, list | tuple):
                streamer = (item for item in streamer)
            assert isinstance(streamer, Generator)
            progress.add_task(task_str)
            first_item = next(streamer)
            streamer = chain((first_item,), streamer)
    print(task_str, end=end)
    return streamer
