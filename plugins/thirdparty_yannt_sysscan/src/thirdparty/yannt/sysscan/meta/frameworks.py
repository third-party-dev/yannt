
def init_framework_entries(db):
    # Frameworks
    db.add(name="pytorch", cmds=["torchrun"], relpaths=[".cache/torch", ".torch"], member_of=["frameworks"])
    tf_cmds=["tensorflow_model_server", "tflite_convert", "saved_model_cli"]
    db.add(name="tensorflow", cmds=tf_cmds, relpaths=[".keras", ".tensorflow"], member_of=["frameworks"])
    db.add(name="jax", member_of=["frameworks"])
    db.add(name="mxnet", member_of=["frameworks"])
    db.add(name="onnx_runtime", cmds=["onnxruntime_perf_test"], relpaths=[".onnx"], member_of=["frameworks"])
    db.add(name="oneflow", member_of=["frameworks"])
    db.add(name="megengine", member_of=["frameworks"])
    db.add(name="ncnn", cmds=["ncnnoptimize"], member_of=["frameworks"])
    # TODO: double check case
    db.add(name="mnn", cmds=["MNNConvert"], relpaths=[".mnn"], member_of=["frameworks"])
    db.add(name="huawei_mindspore",
        cmds=[
            "msprof", "msprof-analyze", "msnpulog", "dump_op", "dump_graph",
            "atc", "msnpureport", "mindspore", "msrun",
        ],
        libs=[],
        member_of=["frameworks"],
    )
