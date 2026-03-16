
def init_quant_entries(db):
    # Quants
    db.add(name="llama.cpp", cmds=['llama'], relpaths=["llama.cpp/models"], member_of=["quants"])
    db.add(name="alpaca.cpp", cmds=["alpaca"], relpaths=["alpaca.cpp/models"], member_of=["quants"])
