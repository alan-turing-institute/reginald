import logging
import os


def get_env_var(var: str, log: bool = True) -> str | None:
    """
    Get environment variable. Logs provided if log is True.

    Parameters
    ----------
    var : str
        Name of environment variable
    log : bool, optional
        Whether or not to log if reading was successful, by default True

    Returns
    -------
    str | None
        Value of environment variable, or None if not found
    """
    if log:
        logging.info(f"Trying to get environment variable '{var}'")
    value = os.environ.get(var)

    if log:
        if value is None:
            logging.warn(
                f"Environment variable '{var}' not found. Can ignore if using default values."
            )
        else:
            logging.info(f"Got environment variable '{var}': {value}")

    return value
