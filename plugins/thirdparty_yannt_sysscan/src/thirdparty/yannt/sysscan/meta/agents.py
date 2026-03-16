
def init_agent_entries(db):
    # Agents
    db.add(name="goose", cmds=["goose"], relpaths=[".cache/goose", ".local/share/goose"], member_of=["agents"])
    db.add(name="autogpt", cmds=["autogpt"], relpaths=[".autogpt"], member_of=["agents"])
    db.add(name="babyagi", relpaths=[".babyagi"], member_of=["agents"])
    db.add(name="langchain", relpaths=[".cache/langchain"], member_of=["agents"])

    # Model Runtimes
    db.add(name="ollama", cmds=["ollama"], relpaths=[".ollama"], member_of=["model_runtimes"])
    db.add(name="lmstudio", relpaths=[".lmstudio"], member_of=["model_runtimes"])
    db.add(name="tensorrt", member_of=["model_runtimes"],
        cmds=["trtexec",], libs=["libnvinfer.so", "libnvinfer_plugin.so",],
        notes=["Inference optimizer and runtime library developed by NVidia"]
    )
