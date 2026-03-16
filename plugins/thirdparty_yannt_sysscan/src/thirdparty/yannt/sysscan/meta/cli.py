
def init_cli_entries(db):
    # CLIs
    db.add(name="copilot", cmds=["github-copilot-cli",], member_of=["cli"],)
