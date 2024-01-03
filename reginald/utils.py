import logging
import os


def get_env_var(var: str, log: bool = True, secret_value: bool = True) -> str | None:
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

    Returns
    -------
    str | None
        Value of environment variable, or None if not found
    """
    if log:
        logging.info(f"Trying to get environment variable '{var}'")
    value = os.getenv(var)

    if log:
        if value is not None:
            if secret_value:
                logging.info(f"Got environment variable '{var}' successfully")
            else:
                logging.info(f"Got environment variable '{var}' successfully: {value}")
        else:
            logging.warn(
                f"Environment variable '{var}' not found. Can ignore if using default values."
            )

    return value
