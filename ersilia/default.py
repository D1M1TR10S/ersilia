from pathlib import Path
import shutil
import os

# EOS environmental variables
EOS = os.path.join(str(Path.home()), "eos")
if not os.path.exists(EOS):
    os.makedirs(EOS)
ROOT = os.path.dirname(os.path.realpath(__file__))
BENTOML_PATH = os.path.join(str(Path.home()), "bentoml")
CHECKSUM_NCHAR = 8
CONDA_ENV_YML_FILE = "environment.yml"
DOCKERFILE_FILE = "Dockerfile"
GITHUB_ORG = "ersilia-os"
GITHUB_ERSILIA_REPO = "ersilia"
CONFIG_JSON = "config.json"
CREDENTIALS_JSON = "credentials.json"
INSTALL_STATUS_FILE = ".install.status"
DOCKER_BENTO_PATH = "/bento"
DOCKERHUB_ORG = "ersiliaos"
DOCKERHUB_LATEST_TAG = "latest"
DEFAULT_DOCKER_PLATFORM = "linux/amd64"
DEFAULT_MODEL_ID = "eos0zzz"
DEFAULT_VENV = "env"
PACKMODE_FILE = "pack_mode.txt"
LOGGING_FILE = "console.log"
CARD_FILE = "card.json"
SILENCE_FILE = ".silence.json"
VERBOSE_FILE = ".verbose.json"
API_SCHEMA_FILE = "api_schema.json"
MODEL_SIZE_FILE = "size.json"
DEFAULT_BATCH_SIZE = 100
FETCHED_MODELS_FILENAME = "fetched_models.txt"
MODEL_CONFIG_FILENAME = "config.json"

# Isaura data lake
H5_EXTENSION = ".h5"
H5_DATA_FILE = "data.h5"
ISAURA_FILE_TAG = "_public"
ISAURA_FILE_TAG_LOCAL = "_local"
ISAURA_GDRIVE = "1LSCMHrCuXUDNH3WRbrLMW2FoiwMCxF2n"
ISAURA_TEAM_GDRIVE = "0AG4WDDaU_00XUk9PVA"
ISAURA_DIR = os.path.join(EOS, "isaura", "lake")

# Other
FEATURE_MERGE_PATTERN = "---"

# Airtable
AIRTABLE_READONLY_API_KEY = "keycTTh5uQ7v2CPbI"
AIRTABLE_MODEL_HUB_BASE_ID = "appgxpCzCDNyGjWc8"
AIRTABLE_MODEL_HUB_TABLE_NAME = "Models"

# URLS
ERSILIA_WEB_URL = "https://ersilia.io"
ERSILIA_MODEL_HUB_URL = "https://ersilia.io/model-hub"

# EOS conda
_resolve_script = "conda_env_resolve.py"
resolve_script = os.path.join(EOS, _resolve_script)
if not os.path.exists(resolve_script):
    shutil.copyfile(
        os.path.join(ROOT, "utils", "supp", _resolve_script), resolve_script
    )

snippet = (
    """
# >>> ersilia >>>
# !! Contents within this block are managed by 'ersilia' !!
eosconda() {
    EOS_MODEL_ENV=$(python %s $2);
    conda $1 $EOS_MODEL_ENV
}

ersilia() {
    if [[ $1 == "conda" ]]; then
        eosconda "${@: 2}"
    elif [[ $1 == "auth" ]]; then
        gh auth "${@: 2}"
    else
        command ersilia "$@"
    fi
}
# <<< ersilia <<<
"""
    % resolve_script
)


def bashrc_path():
    home_path = Path.home()
    rc = os.path.join(home_path, ".bashrc")
    if os.path.exists(rc):
        return rc
    pr = os.path.join(home_path, ".bash_profile")
    if os.path.exists(pr):
        return pr


def has_profile_snippet():
    fn = bashrc_path()
    if not os.path.exists(fn):
        return False
    with open(fn, "r") as f:
        text = f.read()
    if snippet in text:
        return True
    else:
        return False


def bashrc_cli_snippet(overwrite=True):
    """Write a conda snippet in the user profile.

    This function writes on the user profile to create an executable to work
    with conda environments based on model identifiers.

    Motivation behind this function is to define an ersilia CLI.

    Args:
        - overwrite (bool): Overwrite the current bash profile file if the eosconda string is found.
    """
    fn = bashrc_path()
    with open(fn, "r") as f:
        text = f.read()
    if snippet in text:
        if overwrite:
            text = text.split(snippet)[0] + text.split(snippet)[1]
        else:
            return
    with open(fn, "w") as f:
        f.write(text)
    with open(fn, "a+") as f:
        f.write(snippet)
