from ersilia.cli import echo
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.issue_reporting import send_exception_issue
import sys

def throw_ersilia_exception(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as E:
            text = ":triangular_flag: Something went wrong with Ersilia...\n\n"
            text += "{}\n\n".format(self.__class__.__name__)
            echo(text)
            echo("Error message:\n")
            echo(":prohibited: " + str(E), fg="red")
            text = "If this error message is not helpful, open an issue at:\n"
            text += " - https://github.com/ersilia-os/ersilia\n"
            text += "Or feel free to reach out to us at:\n"
            text += " - hello[at]ersilia.io\n\n"
            text += "If you haven't, try to run your command in verbose mode (-v in the CLI)\n\n"
            echo(text)

            if query_yes_no("Would you like to report this error to Ersilia?"):

                if query_yes_no("Would you like to include your last Ersilia command in the issue (for issue reproducibility)?"):
                    sys.stdout.write("Please re-type your last Ersilia command: ")
                    message = input()
                    send_exception_issue(E, message)
                else:
                    send_exception_issue(E, "")

            # if query_yes_no("Would you like to access the log?"):
            #     print("No log info")
            #     # TODO: execute cli logic for [y/n] query and write log to a file
    return inner_function


    