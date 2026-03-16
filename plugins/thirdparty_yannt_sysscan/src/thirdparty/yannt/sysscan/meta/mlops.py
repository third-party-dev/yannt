
def init_mlops_entries(db):
    # ML Ops
    db.add(name="mlflow", cmds=['mlflow'], relpaths=[".mlflow"], member_of=["mlops"])
    db.add(name="wandb", cmds=['wandb'], relpaths=[".wandb"], member_of=["mlops"])
    db.add(name="neptune.ai", relpaths=[".neptune"], member_of=["mlops"])
    db.add(name="clearml", cmds=['clearml-agent'], relpaths=[".clearml"], member_of=["mlops"])
    db.add(name="bentoml", cmds=['bentoml'], relpaths=[".bentoml"], member_of=["mlops"])
    db.add(name="zenml", cmds=['zenml'], relpaths=[".zenml"], member_of=["mlops"])
    db.add(name="dagster", cmds=['dagster'], relpaths=[".dagster"], member_of=["mlops"])
    db.add(name="paddlefleetx", cmds=['fleetx'], relpaths=[".paddle"], member_of=["mlops"])
    db.add(name="paddlepaddle", relpaths=[".paddle"], member_of=["mlops"])
    db.add(name="mindspore", relpaths=[".mindspore"], member_of=["mlops"])
    db.add(name="mindinsight", cmds=['mindinsight'], relpaths=[".mindinsight"], member_of=["mlops"])
    #db.add(name="pai", cmds=['pai'], member_of=["mlops"]) # See sdks
    db.add(name="ti-one", member_of=["mlops"])
