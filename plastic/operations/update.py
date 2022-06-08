from . import command
from ..models import changeset

__CHANGES_FORMAT_SEPARATOR = '#_#'

__incoming_changes_entries = None
__incoming_changes_loaded = False

def update():
    command_result = command.update()

    return None if command_result.success else command_result.output

def get_incoming_changes(changeset):
    global __incoming_changes_loaded

    if not __incoming_changes_loaded and changeset is not None:
        __incoming_changes_loaded = True
        load_incoming_changes(changeset)

    return __incoming_changes_entries

def load_incoming_changes(changeset):
    global __incoming_changes_entries
    __incoming_changes_entries = None

    changeset_branch_result = command.get_changeset_branch(changeset)

    if changeset_branch_result.success:
        changeset_branch = changeset_branch_result.output[0]

        incoming_changes_result = command.get_incoming_changes(changeset, changeset_branch, __CHANGES_FORMAT_SEPARATOR)

        if incoming_changes_result.success:
            __incoming_changes_entries = []

            incoming_changes_result.output.reverse()

            __populate_incoming_changes(incoming_changes_result.output)

        return None if incoming_changes_result.success else incoming_changes_result.output

    return None if changeset_branch_result.success else changeset_branch_result.output

def __populate_incoming_changes(incoming_changes_output):
    for incoming_changes_line in incoming_changes_output:
        incoming_changes_info = incoming_changes_line.split(__CHANGES_FORMAT_SEPARATOR)

        if len(incoming_changes_info) == 4:
            incoming_changes_info.append('')

        if len(incoming_changes_info) == 5:
            __incoming_changes_entries.append(changeset.ChangesetEntry(
                incoming_changes_info[0],
                incoming_changes_info[1],
                incoming_changes_info[2],
                incoming_changes_info[3],
                incoming_changes_info[4]
            ))

def clear_cache():
    global __incoming_changes_entries, __incoming_changes_loaded
    __incoming_changes_entries = None
    __incoming_changes_loaded = False
