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

Instead of a vocabulary, taxonomoy, ontology ... we consider each node its own universe. Dependents should expect that specific universe since its marked the node as a dependency. The dynamic nature of what the provider can ship is advertised based on an array of tags that are specific to the node itself. An AnalysisFactor called thirdparty.yannt.analysis.factors.pparse.Tensors may include tags `['ops', 'weights', 'bias']` for one model and `['ops', 'bias']` for another model. Dependent AnalysisFactors must decide whether they are going to perform their intended operation based on these tags. Subsequent AnalysisFactors will also know if the previous factor was able to complete based on the tags available to it. Therefore, a string of AnalysisFactor classes should always be able to finish execution regardless of whether a node in the middle of the graph failed or not. Note: child factors can determine this based on the results dictionary as well if desired. The expected behavior is specified by each individual node ... but all nodes should provide their resulting tags in the associated results database section.

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

