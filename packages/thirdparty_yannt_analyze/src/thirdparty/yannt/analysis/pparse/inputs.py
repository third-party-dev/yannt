


from thirdparty.yannt.analysis.lib import AnalysisInput

class PparseViewer(AnalysisInput):
    def __init__(self, name = "_init", dependencies = []):
        # Setup base class
        super().__init__(name=name, dependencies=dependencies)
        # Grab config from enclosed class object
        self.factor_config = self.__class__.factor_config
        #breakpoint()


    def missing_input(self):
        if self.input is None:
            return True
        
        if 'path' not in self.input or 'parser' not in self.input:
            return True


    def run(self):
        print(f"Running in {type(self)}:{self.name}")

        '''
            The ideal thing to do in this factor is to use the pparse extraction auto
            detection to determine the file format. That scheme also likely requires
            having to import all the parsers at once.

            A more manual and surgical way to deal with this is to make the target
            file format part of the input.
            
            Note: Creating factor registrations for each type would cause a new procedure
                  for all file formats. This is bad.
                  
            To keep the procedure maintenance manageable, we specify the file format as
            input of the module. File formats are made available by a registry of parsers
            specified in the factor configuration during factor registration. Then the
            input references the parser entry.

            config:
                parser:
                path:

            TODO: `--factor-help input:factor=pparse` should list the current parser registry
        '''

        # Load parser.
        from importlib import import_module
        parser_name = self.get_input()['parser'][-1]
        tgt_path = self.get_input()['path'][-1]

        (module_name, class_name) = self.factor_config['registry'][parser_name]
        parser = getattr(import_module(module_name), class_name)

        print(f"Parsing {parser_name} from: {tgt_path}")

        try:
            obj = parser().open_fpath(tgt_path)
            return obj

        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()

