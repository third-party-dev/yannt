class Product():
    def __init__(self, name="unnamed", cmds=[], libs=[], relpaths=[], ko_prefixes=[], attrs={}, member_of=[], notes=[]):
        self.name = name
        self.commands = cmds
        self.relpaths = relpaths
        self.libs = libs
        self.ko_prefixes = ko_prefixes
        self.attrs = attrs
        self.member_of = member_of
        self.notes = notes


class ProductDatabase():
    def __init__(self):
        self.db = {}

    def add(self, *args, **kwargs):
        if kwargs['name'] in self.db:
            breakpoint()
            raise Exception(f"Product({kwargs['name']}) already in ProductDatabase")
        self.set(kwargs['name'], Product(*args, **kwargs))

    def set(self, name, product):
        self.db[product.name] = product

    def _get_libs(self):
        libs = {}
        for product_name in self.db:
            product = self.db[product_name]
            for lib in product.libs:
                if lib not in libs:
                    libs[lib] = {}
                libs[lib][product_name] = product
        return libs

    def _get_cmds(self):
        cmds = {}
        for product_name in self.db:
            product = self.db[product_name]
            for cmd in product.commands:
                if cmd not in cmds:
                    cmds[cmd] = {}
                cmds[cmd][product_name] = product
        return cmds

    def _get_relpaths(self):
        relpaths = {}
        for product_name in self.db:
            product = self.db[product_name]
            for relpath in product.relpaths:
                if relpath not in relpaths:
                    relpaths[relpath] = {}
                relpaths[relpath][product_name] = product
        return relpaths


def init_database(db):
    from thirdparty.yannt.sysscan.meta.agents import init_agent_entries
    init_agent_entries(db)

    from thirdparty.yannt.sysscan.meta.cli import init_cli_entries
    init_cli_entries(db)

    from thirdparty.yannt.sysscan.meta.drivers import init_driver_entries
    init_driver_entries(db)

    from thirdparty.yannt.sysscan.meta.frameworks import init_framework_entries
    init_framework_entries(db)

    from thirdparty.yannt.sysscan.meta.mlops import init_mlops_entries
    init_mlops_entries(db)

    from thirdparty.yannt.sysscan.meta.quants import init_quant_entries
    init_quant_entries(db)

    from thirdparty.yannt.sysscan.meta.sdk import init_sdk_entries
    init_sdk_entries(db)




DB = ProductDatabase()
# init_database(DB)
