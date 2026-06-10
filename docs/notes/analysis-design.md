## Analysis

We have the pparse parsing framework that is responsible for generating the extraction tree and associated node/parse tree. The parse trees have some partial interpretation by the very nature of the design of their formats. In an effort to make them have more meaningful interfaces like "get_tensor()" or "get_graph()" and return a numpy array or netx graph, we have what pparse calls the "view" wrapper. This is an intermediate representation (IR) or interpretation of the node tree. Is is this IR that should be used by the analysis tools. We intentionally also leak the original parse tree to the analyzer because it may have more insight from the IR into extra bit of information to pull from the parse tree.

I believe, in the big pisture, the correct was to perform the analysis is to generate a directed acyclic graph (DAG) of analyzers that can leverage the inputs and outputs of each other. Initially, this is over-engineered by a mile. We also want researchers to have the ability to simply run "analyze file-x and tell me information-y about it". Perhaps the hybrid are analyzer plugins that a independent from analyzer jobs.

### PLAN

"AnalysisFactors" are nodes in a DAG graph. Each AnalysisFactor declares its dependencies (other AnalysisFactors) and we use a topological sort on the nodes of the graph to make the graph acyclic and each node only needs to be executed once ... sharing its results with all other AnalysisFactors that have declared it as a dependency. The results of a dependency should be accessible via the object class itself (as the key) or a string of the object classes FQN to be translated into the object class itself (as the key).

```python
import sys

def lookup_plugin(module_name: str, class_name: str) -> type:
    module = sys.modules.get(module_name)
    if module is None:
        raise KeyError(f"Module '{module_name}' is not loaded")
    obj = module
    for part in class_name.split("."):
        obj = getattr(obj, part)
    if not isinstance(obj, type):
        raise TypeError(f"'{class_name}' is not a class")
    return obj
```

When all AnalysisFactors have been processed, the resulting dictionary can be dumped with each key being translated in the key's FQN and the AnalysisFactor doing the serialization of its data into an appropriate output format (likely XML).

Pre-defined networks of AnalysisFactors are defined as an AnalysisProcess. AnalysisProcesses are registered into an entrypoint registry with labels that reflect the analysis result a user is after. Because of the nature of the DAG of AnalysisFactors, a user can request multiple analysis results at the same time and the DAGs can merge to produce all of the outputs from all of the AnalysisFactors of all involved nodes. Note: In this case, all results are mixed into a single blob.

For better UX, a user can request a set of AnalysisProcess or request a set of AnalysisReports that will implicitly select the AnalysisProcesses involved and then filter the output to exactly what is in each AnalysisReport. (At the moment, by design), the AnalysisReport will serialize each report independent of the other, meaning there may be duplicate information if multiple reports relay the same or similar information. If a user requests both AnalysisProcess and AnalysisReport, the AnalysisReport is prepended to the AnalysisProcess result.

To recap:

- A user can request one or more AnalysisReports
- A user can request one or more AnalysisProcesses
- An AnalysisProcess is made up of AnalysisFactors.
- Each AnalysisFactor has zero to many AnalysisFactor dependencies.
- An AnalysisReport implies filtered AnalysisProcesses results (or re-interpretation).
- An AnalysisProcess results in all data from all AnalysisFactors.

Note: Pparse should not depend on anything from analyze subcommand. Therefore the analyze subcommand will wrap all first class pparse plugins itself.

#### pparse complexity

The nature of pparse is to take a single file and extract multiple formats and multiple node trees per format. This creates a complex situation for fully automated analysis. Each extraction has results based on the name of the parser. Each AnalysisProcess _could_ trigger on these names and then do its own "I'm going in" thing. We could also do a predicate matching of results to AnalysisProcess or AnalysisResult. We could also do a matching on AnalysisFactor to results and dynamically generate an AnalysisProcess. In practice, I don't know what value we're striving for in any of these situations. Its likely more prudent to stick with "single file can have one to many AnalysisProcesses/AnalysisReports" to keep things manageable until the more complex scenario is better understood.

IDEA #1:

In relation to the above uncertainty, there are certain smaller aspects we should consider when moving forward (to not prohibit any of the above complexity in the future). I'm talking about advertising features or tags of some kind of whats available in a given AnalysisFactor. When we wrap a pparse object, we'll need a definitive way to determine if tensors or the graph is available for reading. There is an inherient challenge with using tags because someone needs to govern the volcabulary that is used and understood across all of the other plugins. For this, I'm considering an AnalysisTaxonomy. Each node can advertise that is supports a named/registered AnalysisTaxonomy and it can list the type of the information it provides in the namespace of the AnalysisTaxonomy.

Example:

AnalysisTaxonomy('mlmodel') -> mlmodel:graph means we're getting a computational graph from an ML model.
AnalysisTaxonomy('excel') -> excel:graph means we're getting a visual graph from a spreadsheet.

At the moment, this is as complex as I want any vocabulary to be in yannt. Trees, overlaps, or ambiguities between taxonomys is getting to far from the problem we're trying to solve.

IDEA #2:

Instead of a vocabulary, taxonomoy, ontology ... we consider each node its own universe. Dependents should expect that specific universe since its marked the node as a dependency. The dynamic nature of what the provider can ship is advertised based on an array of tags that are specific to the node itself. An AnalysisFactor called `thirdparty.yannt.analysis.factors.pparse.Tensors` may include tags `['ops', 'weights', 'bias']` for one model and `['ops', 'bias']` for another model. Dependent AnalysisFactors must decide whether they are going to perform their intended operation based on these tags. Subsequent AnalysisFactors will also know if the previous factor was able to complete based on the tags available to it. Therefore, a string of AnalysisFactor classes should always be able to finish execution regardless of whether a node in the middle of the graph failed or not. Note: child factors can determine this based on the results dictionary as well if desired. The expected behavior is specified by each individual node ... but all nodes should provide their resulting tags in the associated results database section.

### DEMO

```sh
yannt analyze \
  --breakpoint --verbose --log-level \
  --process graph:no-op-naming --process tensors \
  --report fine_tuned --report tensor_metrics \
  --format onnx[schema=/path/to/schema.pb] \
  --target model.onnx
```

- `--process` refers to an AnalysisProcess (registred as entry point)
- `--report` refers to an AnalysisReport (registered as entry point)
- `--format` refers to the target and root of AnalysisProcess (i.e. pparse). (registered as entry point)
- `--target` refers to the target file or path for the parser. (positionals should count as targets too?)
- `--process-help`, `--report-help`, `--format-help` tells argparse to use the associated entrypoint for help output.
- `--process NAME[:key[=value]]` is the pattern for adding options. Repeated uses of `--process NAME` do not add `NAME`, only opts.





### THINGS

What does it mean when we provide a format configuration to AnalysisFramework?
  - Are we configuring a format that will be registered into pparse framework?
  - Are we only saying that we are specifying the parser to use with the target?

**PLAN:** To move forward without limiting the bigger design, gate features with a `simple` subcommand. Simple means we're doing a single "parser extraction's node tree" to file/target (i.e. no multi-extraction recursion).

**PLAN**: In the event that we have 2 plugins that register the same type of object with the same alias, we should indicate to the user they must use a FQN. Users should always be able to use a FQN in place of an alias. FQN and aliases are determined by the presence of a `.` and therefore a `.` must not appear in an alias.

**PLAN**: Each factor, process, and report have reserved parameters:
- `id` - The instance id of the factor/process/report, defaults to `_init`.

**NOTE**: The more I think it through, the more edge cases I'm finding for CLI complexity. Need to flesh out the Python API and revisit. For now, everything will have single instance (not singleton) and have no arguments. Need to flesh out the DAG, factor mapping, process running, report masking ... then revisit CLI, config, and so forth.



### Multi-Input Managements

In the "simple" scenario, we may limit a user request to a single target file/path. How does the AnalysisProcess get the model format type and how do we map that process to that format if there are multiple inputs with multiple formats?

- Run all processes over all inputs?



- Define the input as a process parameter?

yannt analyze --process tensor_metrics:input=model.onnx,fmt=onnx

- We can do it like a qemu network mapping?

`yannt analyze --target onnx:id=mine,path=model.onnx --process tensor_metrics:with=mine,with=another`

```yaml
config:
  framework:
    formats:
      - name: onnx
        module: thirdparty.yannt.analysis.pparse.plugin
        class: OnnxFormat

    factors:
      - name: tensors
        module: thirdparty.yannt.analysis.pparse.plugin
        class: TensorsFactor

    processes:
      - name: basic
        module: thirdparty.yannt.analysis.pparse.plugin
        class: BasicProcess
      - name: second_process
        module: thirdparty.yannt.analysis.pparse.plugin
        class: SecondProcess

    reports:
      - name: tensor_metrics
        module: thirdparty.yannt.analysis.pparse.plugin
        class: TensorMetricsReport

  targets:
    - name: mine
      fmt: onnx
      path: model.onnx
      opts:
        key: value

    - name: another
      fmt: pytorch
      path: model.bin
      opts:
        key: value

  processes:
    - name: tmetric
      process: tensor_metrics
      with: [ mine, another ]
```

Order of precendence (least to most):
- Hard coded defaults
- Installed defaults (entry points)
- Config File
- Environment Variables
- CLI Arguments

AnalysisFactors are really the only generalization we can make. Everything should be constructed of AnalysisFactors and they should be in a DAG. Any simplification of AnalysisProcess feels constricting for reasonable use cases. The most flexible scenario is to define the tree of factors and indicate the required input for the AnalysisProcess. When an analysis process knows its inputs, it may execute. The AnalysisProcess should be definable via Python or Yaml.

```
# Explicitly build a process in CLI
yannt analyze \
  # Indicate we want to load factors
  --load factor:name=pparse,mod=thirdparty.yannt.analysis.pparse.plugin,cls=PparseFormat \
  --load factor:name=tensors,mod=thirdparty.yannt.analysis.pparse.plugin,cls=TensorsFactor \
  # Indicate we want to register factors with process "fine_tuned"
  --factor input:fw=default,proc=fine_tuned,name=model_a,factor=pparse \
  --factor worker:procedure=fine_tuned,name=tensors_a,factor=tensors,dependency=model_a \
  --factor worker:procedure=fine_tuned,name=fine_tuned,factor=fine_tuned \
    # process fine_tuned's fine_tuned factor options continued
    --factor worker:procedure=fine_tuned,name=fine_tuned,dependency=tensor_metrics_a,dependency=tensor_metrics_b \
    --factor worker:procedure=fine_tuned,name=fine_tuned,dependency=graph_a,dependency=graph_b \
  # create process from procedure
  --request process:procedure=fine_tuned,name=fine_tuned \
  # assign input to process
  --input process:name=fine_tuned,factor=model_a,path=model.onnx
  # Note: Once we're done with CLI processing, we implicitly run all processes.


# Define inputs for named process to implicitly run the process.
yannt analyze \
  --load config:path=config.yaml \
  --input target:process=fine_tuned,name=model_a,path=model.onnx \
  --input target:process=fine_tuned,name=model_b,path=model.onnx


# Define inputs for named report to implicitly run the process via a report.
# Add report specific option for output.
yannt analyze \
  --load config:path=config.yaml \
  --input target:report=fine_tuned,name=model_a,path=model.onnx \
  --input target:report=fine_tuned,name=model_b,path=model.onnx \
  --report output:report=fine_tuned,fmt=xml,path=report.xml
```


```yaml

framework:
  factors:
    - name: pparse
      module: thirdparty.yannt.analysis.pparse.plugin
      class: PparseFormat
      config:
        registry:
          onnx: pparse.onnx
          pytoroch: pparse.pytorch

    - name: tensors
      module: thirdparty.yannt.analysis.pparse.plugin
      class: TensorsFactor

    - name: graph
      module: thirdparty.yannt.analysis.pparse.plugin
      class: GraphFactor

    - name: tensor_metrics
      module: thirdparty.yannt.analysis.pparse.plugin
      class: TensorsMetrics

    - name: fine_tuned
      module: thirdparty.yannt.analysis.pparse.plugin
      class: FineTuned

procedure:
  - name: fine_tuned
    inputs:
      model_a:
        factor: pparse

      model_b:
        factor: pparse

    factors:
      - name: tensors_a
        factor: tensors
        dependencies:
        - model_a
      
      - name: graph_a
        factor: graph
        dependencies:
        - model_a
      
      - name: tensor_metrics_a
        factor: tensor_metrics
        dependencies:
        - tensors_a

      - name: tensors_b
        factor: tensors
        dependencies:
        - model_b
      
      - name: graph_b
        factor: graph
        dependencies:
        - model_b
      
      - name: tensor_metrics_b
        factor: tensor_metrics
        dependencies:
        - tensors_b

      - name: fine_tuned
        factor: fine_tuned
        dependencies:
        - tensor_metrics_a
        - tensor_metrics_b
        - graph_a
        - graph_b
```

```python

def pparse_plugin(cls_name):
  return ('thirdparty.yannt.analysis.pparse.plugin', cls_name)

config = { 'registry': { 'onnx': 'pparse.onnx', 'pytoroch': 'pparse.pytorch' } }
framework.register_factor('pparse', pparse_plugin('PparseFormat'), config)

framework.register_factor('tensors', pparse_plugin('TensorsFactor'))
framework.register_factor('graph', pparse_plugin('GraphFactor'))
framework.register_factor('tensor_metrics', pparse_plugin('TensorsMetrics'))
framework.register_factor('fine_tuned', pparse_plugin('FineTuned'))

fine_tuned_process = AnalysisProcedure()
fine_tuned_process.add_input('model_a', factor=framework.factor['pparse'])
fine_tuned_process.add_input('model_b', factor=framework.factor['pparse'])

fine_tuned_process.add_factor('tensors_a', factor=framework.factor['tensors'], dependencies=['model_a'])
fine_tuned_process.add_factor('graph_a', factor=framework.factor['graph'], dependencies=['model_a'])
fine_tuned_process.add_factor('tensor_metrics_a', factor=framework.factor['tensor_metrics'], dependencies=['tensors_a'])
fine_tuned_process.add_factor('tensors_b', factor=framework.factor['tensors'], dependencies=['model_b'])
fine_tuned_process.add_factor('graph_b', factor=framework.factor['graph'], dependencies=['model_b'])
fine_tuned_process.add_factor('tensor_metrics_b', factor=framework.factor['tensor_metrics'], dependencies=['tensors_b'])

fine_tuned_process.add_factor('fine_tuned', 
  factor=framework.factor['fine_tuned'],
  dependencies=['tensor_metrics_a', 'tensor_metrics_b', 'graph_a', 'graph_b'],
)

framework.register_process('fine_tuned', fine_tuned_process)

```





We can optimize merging of the above and another process by computing the lineage with root+input and deduplicate nodes across processes:

```python
def compute_lineage(node, parent_map, root_inputs):
    ancestors = set()

    def collect(n):
        for parent in parent_map.get(n, []):
            if parent not in ancestors:
                ancestors.add(parent)
                collect(parent)

    collect(node)

    sorted_ancestors = topological_sort(ancestors, parent_map)

    # substitute root nodes with (node, input) pairs
    def with_input(n):
        if n not in parent_map or not parent_map[n]:
            return (n, n.get_input_value())
        return n

    return (*[with_input(n) for n in sorted_ancestors], node)


def topological_sort(nodes, parent_map):
    result = []
    visited = set()

    def visit(n):
        if n in visited:
            return
        visited.add(n)
        for parent in sorted(parent_map.get(n, []), key=lambda n: n.id):
            visit(parent)
        result.append(n)

    for node in sorted(nodes, key=lambda n: n.id):
        visit(node)

    return tuple(result)
```

Given: `R1(input_a) -> A -> C` and `R2(input_b) -> B -> C`
Result: `compute_lineage(C) == ((R1, input_a), (R2, input_b), A, B, C)`
And `((R1, input_a), (R2, input_b), A, B, C)` becomes the unique ID for the node and we can remove any duplicates.

**Note**: This only works if all nodes in the graph only read from dependencies and not outside inputs.



## Impl Notes

PyTorch, recursive tensor construction:

```sh
yannt analyze --breakpoint --config config.yaml \
  --request process:name=mine,proc=fine_tuned \
  --input process:name=mine,factor=model_a,parser=onnx,path=models/yolo/yolov5su.onnx \
  --input process:name=mine,factor=model_b,parser=pytorch,path=models/bert/pt/bert-AutoModel.complete.pt
```

PyTorch, linear tensor construction:

```sh
yannt analyze --breakpoint --config config.yaml \
  --request process:name=mine,proc=fine_tuned \
  --input process:name=mine,factor=model_a,parser=onnx,path=models/yolo/yolov5su.onnx \
  --input process:name=mine,factor=model_b,parser=pytorch,path=models/bert/pt/bert-AutoModel.params.pt
```

PyTorch, failing tensor construction:

```sh
yannt analyze --breakpoint --config config.yaml \
  --request process:name=mine,proc=fine_tuned \
  --input process:name=mine,factor=model_a,parser=onnx,path=models/yolo/yolov5su.onnx \
  --input process:name=mine,factor=model_b,parser=pytorch,path=models/yolo/yolov5su.pt
```

BUG: pparse PyTorch fails to get tensors from yolov5su.pt
- pparse assumes NewCall or ReduceCall, but yolo returns dict, need to know how its serialized.


### Onnx Op Prov

- `node._value['domain']` - namespace/organization that created model (very optional)
- `node._value['opset_import']._value['version']` - onnx opset
- `node._value['metadata_props']` - dict about model (very optional)

- `node._value['graph']` - Graph
  - `node._value['graph']._value['initializer']` - Tensor Values
  - `node._value['graph']._value['node']` - Nodes in the graph


- `op_type`






<!-- The parser framework includes a registry of parsers fed to an initial extraction that represents data from a file. The extraction finds a parser from the registry that can parse its data into a parse tree of decomposed data structure information. The parse tree is mostly made up of a common node structure that _may_ contain context (the data required to perform parsing) and it has a value that _may_ be loaded. If the value is dereferenced and the data is not loaded, it will attempt to parse the data from the context. If the context does not exist, it'll go up the parse tree looking for the next available context to start the parsing replay. Parse trees can contain data that the current parser can not parse. In that case, the encapsulated data becomes a child extraction. Once this extraction exists, the process is repeated by finding a parser to process the child extraction's data. -->

## Progressive Parsing Concepts

When you point the parser at a file, it doesn't try to understand the while thing at once. It starts with an extraction or a chunk of raw data and a question: What is this? To answer that, the tool looks up available format parsers in a registry. The registry finds the parser that recognizes the data and hands it over. That parser decomposes the data into a parse tree (a structured representation of what was found).

Most nodes in the parse tree share a common structure. The nodes carry a value and optionally a context (the data needed to product the value). The value isn't loaded until you ask for it. When you do, if the data isn't there, the node looks to its context. If the context isn't there either, it walks up the tree until it finds one and replays parsing from that point. This means the tree can represent a file far larger than available memory. Only the parts you touch are ever fully resolved is another way to think of it.

Some nodes contain data the current parser doesn't recognize. Instead of failing, that data becomes a child extraction and the whole process repeats. A new parser is found and another subtree is built. The format doesn't need to me monolithic for the tool to make progress.



<!-- The analysis framework contains analysis procedures. Analysis procedures contain analysis factors. Analysis factors that have no dependencies are analysis inputs and usually represent external resources like pparse results. The pparse results are presented in a common API so that most derived factors do not need to know the format of the model they are performing analysis on. Analysis processes are collections of factors from an analysis procedure that are sorted and then executed. The analysis process has a dictionary where each key represents a factor instance's output. Analysis reports are associated with a procedure and when executed create their own process and then filter the information down to only what the report (or user) wants a summary on. -->


## Declarative Analysis Concepts

Reading and parsing the file gives you structure, but the structure alone does not answer: Does this contain executable code?, Where do the weights come from? Answering those requires combining observations and derived observations.

The analysis framework is built around that derived dependency problem. An analysis procedure define a network of factors (i.e. observations), each one a discrete piece of code that declares what it produces and what it needs to process. Factors with no dependencies are inputs. A common input factor is one that reaches into the parser results for initial observations. Everything built on top of an input factor are worker factors. All worker factors receive the outputs of other factors and produce something more specific.

Most derived worker factors don't need to know what model format they're processing because the parser results are presented through a common (domain specific) APIm so the same analysis logic works across most formats.

When you run an analysis process, the framework sorts the factors by their dependencies and executes them in order. The results are added to a dictionary keyed by the factor instance name. The dictionary becomes a complete record of every observation made.

An analysis report is a filter over that process. The report defines which factors matter for a particular question, runs the process, and filters the output down to only what the user asked for. The full analysis happens either way, the report decides what gets exposed.
