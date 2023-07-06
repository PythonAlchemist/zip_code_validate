import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_zip_data(path: str) -> pd.DataFrame:
    """Create a df from the zip_data.csv file indexed by zip and zip4"""

    try:
        df = pd.read_csv(path)
        df.set_index(["PHYSICAL ZIP", "PHYSICAL ZIP 4"], inplace=True)
        return df
    except FileNotFoundError:
        log.error("path not found")
        raise
    except Exception as e:
        log.error(e)
        raise


def parse_zip_str(zip_str: str) -> tuple:
    zip, zip4 = None, None
    zip_str = zip_str.strip()

    if len(zip_str) == 5 and zip_str.isdigit():
        zip = int(zip_str)
    elif len(zip_str) == 9 and zip_str.isdigit():
        zip, zip4 = int(zip_str[:5]), int(zip_str[5:])
    elif "-" in zip_str and len(zip_str.split("-")) == 2:
        zip, zip4 = zip_str.split("-")
        zip, zip4 = int(zip), int(zip4)
        if len(str(zip4)) != 4:
            zip4 = None
    else:
        log.error(f"input zip format is not valid: {zip_str}")

    return zip, zip4


def check_valid_zip(df: pd.DataFrame, zip_obj: tuple, return_meta: bool = False):
    """Check if the zip or zip4 are valid"""

    zip, zip4 = zip_obj

    if zip4 and len(str(zip4)) != 4:
        log.info("input zip4 is not valid")
        return 0

    # both zip and zip4 are invalid
    if not zip and not zip4:
        log.info("input zip is not valid")
        return 0

    elif zip4 and not zip:
        log.info("input zip is not valid")
        return 0
    # 5 digit zip
    elif zip and not zip4:
        try:
            return df.loc[zip] if return_meta else 1
        except KeyError:
            log.info("input zip is not valid")
            return 0
    # 9 digit zip
    elif zip and zip4:
        try:
            return df.loc[zip, zip4] if return_meta else 1
        except KeyError:
            log.info("input zip4 is not valid")
            return 0
    # invalid zip
    else:
        log.info("input zip format is not valid")
        return 0
