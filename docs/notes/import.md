
# Heading

```xml
<!-- File -->
<source type="file">
    <path>/path/to/model.onnx</path>
    <offset>0</offset>
    <length>104857600</length>
</source>

<!-- URL -->
<source type="url">
    <href>https://example.com/model.onnx</href>
    <offset>0</offset>
    <length>104857600</length>
</source>

<!-- Buffer (inline data, e.g. base64) -->
<source type="buffer">
    <encoding>base64</encoding>
    <data>SGVsbG8gV29ybGQ=</data>
</source>

<!-- Buffer by reference (e.g. named/shared buffer in a larger context) -->
<source type="buffer_ref">
    <ref>my_buffer_id</ref>
    <offset>0</offset>
    <length>104857600</length>
</source>
```

Several issues to address when expressing pparse state in XML:

- I want to clearly show the extraction tree with associated datasources, result references, and child extractions.
  - Flattening this tree takes the value from having the XML in an XML viewer.
  - TODO: Are there viewers that do cross-references elegantly?
- I want to clearly show the relationships between nodes and their values. While I don't need node trees to clutter the extraction result lists themselves, node trees should not be flattened within a single result.
  - Node contexts however are not intended for humans and therefore can be flattened into a following section.

```xml
<pparse>
    <!-- root extraction -->
    <extraction>
        <!-- every extraction has a data source -->
        <datasource type="FileData" />
            <!-- optional? digest -->
            <digest type="sha1" length="123">sha1_here</digest>

            <!-- for when data source is dependent on parent result -->
            <!-- TODO: use the result ref and use a path through nodes that uses node.value.value -->
            <from_parent result="zip">
                <!-- the exact (relative) path to the node value is given as xpath -->
                <!-- ! no good because we'll need to node.value.value.value our way there. -->
                <result_xpath>//Node/value/Node</result_xpath>
            </from_parent>

            <!-- datasource type specific options -->
            <extra /><!-- XmlEntry -->
        </datasource>

        <results>
            <!-- result_ref points to a root node in /job/results -->
            <result_ref id="" />
        </results>

        <child_extractions>
            <!-- we do not use extraction references here because we want to navigate the relationships -->
            <extraction />
        </child_extractions>
    </extraction>

    <results>
        <!-- each result is named after the parser that parsed it. -->
        <!-- results contain the reference referred to by the extraction/results -->
        <!-- TODO: when parsing XML, match every result_ref with this result object in XmlNode. -->
        <result name="zip" id="1">
            <!-- node may have a type="", but it implicitly pparse.Node. -->
            <!-- node should have offset, may have length ... equates to the node's reader -->
            <node offset="0" length="164892">
                <!-- (optional) for context parse replay (i.e. context initialization) -->
                <!-- when we don't know how to replay parsing, we go further up the tree until we do. -->
                <!-- if we reach root without seeing context init args, we let the parser decide. -->
                <!-- TODO: determine what this looks like in python -->
                <context parser="zip" state="complete" />
                <!-- every node has a value or `<unloaded_value />` -->
                <value type="node">
                    <node offset="10" length="164882">
                        <value type="map">
                            <entry type="int" name="int_key">42</entry>
                            <entry type="float" name="float_key">3.14</entry>
                            <entry type="str" name="str_key">dance</entry>
                            <!-- entry is inherently json friendly, therefore type="json" -->
                            <!--   assumes the return should use json.loads -->
                            <entry type="json" name="json_key">
                                [1, 8, 16, 16]
                            </entry>
                            <!-- "normal" entry of type="list" has more entries -->
                            <entry type="list" name="list_key">
                                <entry type="int">1</entry>
                                <entry type="int">8</entry>
                                <entry type="int">16</entry>
                                <entry type="int">16</entry>
                            </entry>
                        </value>
                        <value type="node|map|list|str|int|float">value_here</value>
                    </node>
                </value>
            </node>
        </result>
    </results>
</pparse>
```
