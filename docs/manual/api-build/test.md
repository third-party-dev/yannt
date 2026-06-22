Attribute: AGAIN = 1
Attribute: ASCEND = 2
Attribute: NEXT = 3

<a id="thirdparty.pparse.lib.EndOfDataException"></a>

--------------------------------------------------------------
### EndOfDataException
--------------------------------------------------------------

`class EndOfDataException(Exception)`

#### Attributes



#### Functions



<a id="thirdparty.pparse.lib.EndOfNodeException"></a>

--------------------------------------------------------------
### EndOfNodeException
--------------------------------------------------------------

`class EndOfNodeException(Exception)`

#### Attributes



#### Functions



<a id="thirdparty.pparse.lib.UnsupportedFormatException"></a>

--------------------------------------------------------------
### UnsupportedFormatException
--------------------------------------------------------------

`class UnsupportedFormatException(Exception)`

#### Attributes



#### Functions



<a id="thirdparty.pparse.lib.BufferFullException"></a>

--------------------------------------------------------------
### BufferFullException
--------------------------------------------------------------

`class BufferFullException(Exception)`

#### Attributes



#### Functions



<a id="thirdparty.pparse.lib.NodeContext"></a>

--------------------------------------------------------------
### NodeContext
--------------------------------------------------------------

`class NodeContext()`

#### Attributes

| Attribute    | Default      |
| ------------ | ------------ |
| _reader      | reader.dup() |
| _state_stack | []           |
| _parent      | parent       |
| _start       | self.tell()  |
| _end         | None         |
| _parser      | parser       |
| _descendants | []           |

#### Functions

| Prototype                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.NodeContext.__init__)``(parent: Optional[Node], reader: Reader, parser: Parser) -> None |
| def [`parent`](#thirdparty.pparse.lib.NodeContext.parent)``() -> Optional[Node]                                                 |
| def [`parent_ctx`](#thirdparty.pparse.lib.NodeContext.parent_ctx)``() -> Optional[NodeContext]                                  |
| def [`reader`](#thirdparty.pparse.lib.NodeContext.reader)``() -> Reader                                                         |
| def [`parser`](#thirdparty.pparse.lib.NodeContext.parser)``() -> Parser                                                         |
| def [`_init_state`](#thirdparty.pparse.lib.NodeContext._init_state)``(state: Type[Any]) -> None                                 |
| def [`_init_states`](#thirdparty.pparse.lib.NodeContext._init_states)``(states: List[Type[Any]]) -> None                        |
| def [`_next_state`](#thirdparty.pparse.lib.NodeContext._next_state)``(state: Type[Any]) -> None                                 |
| def [`_next_states`](#thirdparty.pparse.lib.NodeContext._next_states)``(states: List[Type[Any]]) -> None                        |
| def [`state`](#thirdparty.pparse.lib.NodeContext.state)``() -> Any                                                              |
| def [`_pop_state`](#thirdparty.pparse.lib.NodeContext._pop_state)``() -> Any                                                    |
| def [`set_remaining`](#thirdparty.pparse.lib.NodeContext.set_remaining)``(length: int) -> None                                  |
| def [`mark_end`](#thirdparty.pparse.lib.NodeContext.mark_end)``(node: Node) -> None                                             |
| def [`mark_field_start`](#thirdparty.pparse.lib.NodeContext.mark_field_start)``() -> None                                       |
| def [`field_start`](#thirdparty.pparse.lib.NodeContext.field_start)``() -> int                                                  |
| def [`dup`](#thirdparty.pparse.lib.NodeContext.dup)``() -> Reader                                                               |
| def [`tell`](#thirdparty.pparse.lib.NodeContext.tell)``() -> int                                                                |
| def [`seek`](#thirdparty.pparse.lib.NodeContext.seek)``(*args: Any = (), **kwargs: Any = {}) -> Any                             |
| def [`skip`](#thirdparty.pparse.lib.NodeContext.skip)``(*args: Any = (), **kwargs: Any = {}) -> Any                             |
| def [`peek`](#thirdparty.pparse.lib.NodeContext.peek)``(*args: Any = (), **kwargs: Any = {}) -> bytes                           |
| def [`read`](#thirdparty.pparse.lib.NodeContext.read)``(*args: Any = (), **kwargs: Any = {}) -> bytes                           |
| def [`left`](#thirdparty.pparse.lib.NodeContext.left)``() -> int                                                                |
Attribute: UNLOADED_VALUE = UnloadedValue()

<a id="thirdparty.pparse.lib.RecursionControl"></a>

--------------------------------------------------------------
### RecursionControl
--------------------------------------------------------------

`class RecursionControl()`

#### Attributes

| Attribute      | Default             |
| -------------- | ------------------- |
| MAX_DEPTH      | 9223372036854775807 |
| cur_depth      | 0                   |
| max_seen_depth | 0                   |
| min_depth      | min_depth           |
| max_depth      | max_depth           |
| cb             | callback            |

#### Functions

| Prototype                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.RecursionControl.__init__)``(min_depth: int = 0, max_depth: int = MAX_DEPTH, callback: Optional[Callable[[Node], bool]] = None) -> None |
| def [`stopped`](#thirdparty.pparse.lib.RecursionControl.stopped)``(node: Node) -> bool                                                                                          |
| def [`increase_depth`](#thirdparty.pparse.lib.RecursionControl.increase_depth)``(amount: int = 1) -> None                                                                       |
| def [`decrease_depth`](#thirdparty.pparse.lib.RecursionControl.decrease_depth)``(amount: int = 1) -> None                                                                       |
| def [`current_depth`](#thirdparty.pparse.lib.RecursionControl.current_depth)``() -> int                                                                                         |
| def [`deepest_depth`](#thirdparty.pparse.lib.RecursionControl.deepest_depth)``() -> int                                                                                         |

<a id="thirdparty.pparse.lib.Node"></a>

--------------------------------------------------------------
### Node
--------------------------------------------------------------

`class Node()`

#### Attributes

| Attribute | Default |
| --------- | ------- |
| value     | None    |

#### Functions

| Prototype                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------- |
| def [`clear_ctx`](#thirdparty.pparse.lib.Node.clear_ctx)``() -> Node                                             |
| def [`ctx`](#thirdparty.pparse.lib.Node.ctx)``() -> NodeContext                                                  |
| def [`dump`](#thirdparty.pparse.lib.Node.dump)``(depth: int = 0, step: int = 2, dumper: Any = None) -> None      |
| def [`from_xml`](#thirdparty.pparse.lib.Node.from_xml)``(src_xml: Any, ctx_ref: Any) -> Optional[Node]           |
| def [`length`](#thirdparty.pparse.lib.Node.length)``() -> int                                                    |
| def [`load`](#thirdparty.pparse.lib.Node.load)``(recursion: Optional[RecursionControl] = None) -> Optional[Node] |
| def [`set_length`](#thirdparty.pparse.lib.Node.set_length)``(length: int) -> Node                                |
| def [`tell`](#thirdparty.pparse.lib.Node.tell)``() -> int                                                        |
| def [`unload`](#thirdparty.pparse.lib.Node.unload)``() -> None                                                   |

<a id="thirdparty.pparse.lib.Reader"></a>

--------------------------------------------------------------
### Reader
--------------------------------------------------------------

`class Reader()`

#### Attributes



#### Functions

| Prototype                                                                |
| ------------------------------------------------------------------------ |
| def [`dup`](#thirdparty.pparse.lib.Reader.dup)``() -> Reader             |
| def [`tell`](#thirdparty.pparse.lib.Reader.tell)``() -> int              |
| def [`seek`](#thirdparty.pparse.lib.Reader.seek)``(offset: int) -> Any   |
| def [`skip`](#thirdparty.pparse.lib.Reader.skip)``(length: int) -> Any   |
| def [`peek`](#thirdparty.pparse.lib.Reader.peek)``(length: int) -> bytes |
| def [`read`](#thirdparty.pparse.lib.Reader.read)``(length: int) -> bytes |

<a id="thirdparty.pparse.lib.Cursor"></a>

--------------------------------------------------------------
### Cursor
--------------------------------------------------------------

`class Cursor(Reader)`

#### Attributes

| Attribute | Default |
| --------- | ------- |
| _data     | data    |
| _offset   | offset  |

#### Functions

| Prototype                                                                                      |
| ---------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.Cursor.__init__)``(data: Any, offset: int = 0) -> None |
| def [`cursor`](#thirdparty.pparse.lib.Cursor.cursor)``() -> Cursor                             |
| def [`dup`](#thirdparty.pparse.lib.Cursor.dup)``() -> Cursor                                   |
| def [`tell`](#thirdparty.pparse.lib.Cursor.tell)``() -> int                                    |
| def [`seek`](#thirdparty.pparse.lib.Cursor.seek)``(offset: int) -> Any                         |
| def [`skip`](#thirdparty.pparse.lib.Cursor.skip)``(length: int) -> Any                         |
| def [`peek`](#thirdparty.pparse.lib.Cursor.peek)``(length: int) -> bytes                       |
| def [`read`](#thirdparty.pparse.lib.Cursor.read)``(length: int, mode: Any = None) -> bytes     |

<a id="thirdparty.pparse.lib.Range"></a>

--------------------------------------------------------------
### Range
--------------------------------------------------------------

`class Range(Reader)`

#### Attributes

| Attribute     | Default      |
| ------------- | ------------ |
| _start_cursor | cursor.dup() |

#### Functions

| Prototype                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.Range.__init__)``(cursor: Cursor, length: int, offset: int = -1) -> None      |
| def [`_init`](#thirdparty.pparse.lib.Range._init)``(start_offset: int, length: int, current_offset: int = -1) -> None |
| def [`cursor`](#thirdparty.pparse.lib.Range.cursor)``() -> Cursor                                                     |
| def [`dup`](#thirdparty.pparse.lib.Range.dup)``() -> Range                                                            |
| def [`truncate`](#thirdparty.pparse.lib.Range.truncate)``(new_length: int) -> Range                                   |
| def [`length`](#thirdparty.pparse.lib.Range.length)``() -> int                                                        |
| def [`left`](#thirdparty.pparse.lib.Range.left)``() -> int                                                            |
| def [`valid_offset`](#thirdparty.pparse.lib.Range.valid_offset)``(offset: int) -> bool                                |
| def [`tell`](#thirdparty.pparse.lib.Range.tell)``() -> int                                                            |
| def [`seek`](#thirdparty.pparse.lib.Range.seek)``(offset: int) -> int                                                 |
| def [`_adjust_length`](#thirdparty.pparse.lib.Range._adjust_length)``(length: int) -> int                             |
| def [`skip`](#thirdparty.pparse.lib.Range.skip)``(length: int) -> Any                                                 |
| def [`peek`](#thirdparty.pparse.lib.Range.peek)``(length: int) -> bytes                                               |
| def [`read`](#thirdparty.pparse.lib.Range.read)``(length: int) -> bytes                                               |

<a id="thirdparty.pparse.lib.Data"></a>

--------------------------------------------------------------
### Data
--------------------------------------------------------------

`class Data()`

#### Attributes



#### Functions

| Prototype                                                                              |
| -------------------------------------------------------------------------------------- |
| def [`open`](#thirdparty.pparse.lib.Data.open)``(offset: int = 0) -> Cursor            |
| def [`peek`](#thirdparty.pparse.lib.Data.peek)``(cursor: Cursor, length: int) -> bytes |
| def [`seek`](#thirdparty.pparse.lib.Data.seek)``(cursor: Cursor) -> int                |
| def [`read`](#thirdparty.pparse.lib.Data.read)``(cursor: Cursor, length: int) -> bytes |

<a id="thirdparty.pparse.lib.HttpCachedData"></a>

--------------------------------------------------------------
### HttpCachedData
--------------------------------------------------------------

`class HttpCachedData(Data)`

#### Attributes

| Attribute        | Default                                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| CHUNK_SIZE       | 4096 * 256                                                                                            |
| MAX_CHUNKS       | 1024                                                                                                  |
| _session         | session or requests.Session()                                                                         |
| length           | int(response.headers['Content-Length'])                                                               |
| _supports_ranges | response.headers.get('Accept-Ranges', 'none').lower() == 'bytes'                                      |
| httpdata         | _HttpCachedData(url, chunk_size=chunk_size, chunk_max_count=chunk_max_count, session=(self._session)) |

#### Functions

| Prototype                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| def [`__init__`](#thirdparty.pparse.lib.HttpCachedData.__init__)``(url: str, chunk_size: int = CHUNK_SIZE, chunk_max_count: int = MAX_CHUNKS, session: Optional[Any] = None) -> None |
| def [`peek`](#thirdparty.pparse.lib.HttpCachedData.peek)``(cursor: Cursor, length: int) -> bytes                                                                                     |

<a id="thirdparty.pparse.lib.HttpRangeData"></a>

--------------------------------------------------------------
### HttpRangeData
--------------------------------------------------------------

`class HttpRangeData(Data)`

#### Attributes

| Attribute | Default             |
| --------- | ------------------- |
| _url      | url                 |
| _session  | requests.Session()  |
| length    | self._load_length() |

#### Functions

| Prototype                                                                                            |
| ---------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.HttpRangeData.__init__)``(url: Optional[str] = None) -> None |
| def [`_load_length`](#thirdparty.pparse.lib.HttpRangeData._load_length)``() -> int                   |
| def [`peek`](#thirdparty.pparse.lib.HttpRangeData.peek)``(cursor: Cursor, length: int) -> bytes      |
| def [`seek`](#thirdparty.pparse.lib.HttpRangeData.seek)``(cursor: Cursor) -> int                     |
| def [`read`](#thirdparty.pparse.lib.HttpRangeData.read)``(cursor: Cursor, length: int) -> bytes      |

<a id="thirdparty.pparse.lib.FileData"></a>

--------------------------------------------------------------
### FileData
--------------------------------------------------------------

`class FileData(Data)`

#### Attributes

| Attribute | Default          |
| --------- | ---------------- |
| _path     | path             |
| length    | None             |
| _fobj     | open(path, 'rb') |

#### Functions

| Prototype                                                                                        |
| ------------------------------------------------------------------------------------------------ |
| def [`__init__`](#thirdparty.pparse.lib.FileData.__init__)``(path: Optional[str] = None) -> None |
| def [`peek`](#thirdparty.pparse.lib.FileData.peek)``(cursor: Cursor, length: int) -> bytes       |
| def [`seek`](#thirdparty.pparse.lib.FileData.seek)``(cursor: Cursor) -> int                      |
| def [`read`](#thirdparty.pparse.lib.FileData.read)``(cursor: Cursor, length: int) -> bytes       |
| def [`from_xml`](#thirdparty.pparse.lib.FileData.from_xml)``(xml_src: Any) -> FileData           |
| def [`to_xml`](#thirdparty.pparse.lib.FileData.to_xml)``() -> str                                |

<a id="thirdparty.pparse.lib.FileMmapData"></a>

--------------------------------------------------------------
### FileMmapData
--------------------------------------------------------------

`class FileMmapData(Data)`

#### Attributes

| Attribute | Default                                                      |
| --------- | ------------------------------------------------------------ |
| _path     | path                                                         |
| length    | None                                                         |
| _fobj     | open(path, 'rb')                                             |
| _mmap     | mmap.mmap(self._fobj.fileno(), 0, access=(mmap.ACCESS_READ)) |
| _mem      | memoryview(self._mmap)                                       |

#### Functions

| Prototype                                                                                                             |
| --------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.FileMmapData.__init__)``(path: Optional[str] = None) -> None                  |
| def [`_load_length`](#thirdparty.pparse.lib.FileMmapData._load_length)``() -> None                                    |
| def [`peek`](#thirdparty.pparse.lib.FileMmapData.peek)``(cursor: Cursor, length: int) -> memoryview                   |
| def [`seek`](#thirdparty.pparse.lib.FileMmapData.seek)``(cursor: Cursor) -> int                                       |
| def [`read`](#thirdparty.pparse.lib.FileMmapData.read)``(cursor: Cursor, length: int, mode: Any = None) -> memoryview |

<a id="thirdparty.pparse.lib.BytesIoData"></a>

--------------------------------------------------------------
### BytesIoData
--------------------------------------------------------------

`class BytesIoData(Data)`

#### Attributes

| Attribute | Default                         |
| --------- | ------------------------------- |
| _bytes_io | bytes_io                        |
| length    | len(self._bytes_io.getbuffer()) |

#### Functions

| Prototype                                                                                                      |
| -------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.BytesIoData.__init__)``(bytes_io: Optional[io.BytesIO] = None) -> None |
| def [`_load_length`](#thirdparty.pparse.lib.BytesIoData._load_length)``() -> None                              |
| def [`open`](#thirdparty.pparse.lib.BytesIoData.open)``(offset: int = 0) -> Cursor                             |
| def [`peek`](#thirdparty.pparse.lib.BytesIoData.peek)``(cursor: Cursor, length: int) -> bytes                  |
| def [`seek`](#thirdparty.pparse.lib.BytesIoData.seek)``(cursor: Cursor) -> int                                 |
| def [`read`](#thirdparty.pparse.lib.BytesIoData.read)``(cursor: Cursor, length: int) -> bytes                  |

<a id="thirdparty.pparse.lib.Extraction"></a>

--------------------------------------------------------------
### Extraction
--------------------------------------------------------------

`class Extraction()`

#### Attributes

| Attribute    | Default |
| ------------ | ------- |
| _source      | source  |
| _name        | name    |
| _parser      | {}      |
| _result      | {}      |
| _extractions | []      |

#### Functions

| Prototype                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.Extraction.__init__)``(name: Optional[str] = None, source: Optional[Extraction] = None) -> None |
| def [`name`](#thirdparty.pparse.lib.Extraction.name)``() -> Optional[str]                                                               |
| def [`set_name`](#thirdparty.pparse.lib.Extraction.set_name)``(name: str) -> Extraction                                                 |
| def [`add_result`](#thirdparty.pparse.lib.Extraction.add_result)``(id: Any, root_node: Optional[Node]) -> None                          |
| def [`add_parser`](#thirdparty.pparse.lib.Extraction.add_parser)``(id: str, parser: Optional[Parser]) -> None                           |
| def [`has_parser`](#thirdparty.pparse.lib.Extraction.has_parser)``(parser_id: str) -> bool                                              |
| def [`discover_parsers`](#thirdparty.pparse.lib.Extraction.discover_parsers)``(parser_registry: Dict[str, Any]) -> Extraction           |
| def [`open`](#thirdparty.pparse.lib.Extraction.open)``() -> Reader                                                                      |
| def [`scan_data`](#thirdparty.pparse.lib.Extraction.scan_data)``() -> Extraction                                                        |
| def [`from_xml`](#thirdparty.pparse.lib.Extraction.from_xml)``(xml_src: Any, xml_root: Any) -> Extraction                               |
| def [`to_xml`](#thirdparty.pparse.lib.Extraction.to_xml)``() -> str                                                                     |

<a id="thirdparty.pparse.lib.BytesExtraction"></a>

--------------------------------------------------------------
### BytesExtraction
--------------------------------------------------------------

`class BytesExtraction(Extraction)`

#### Attributes

| Attribute | Default |
| --------- | ------- |
| _reader   | reader  |

#### Functions

| Prototype                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.BytesExtraction.__init__)``(name: Optional[str] = None, source: Optional[Extraction] = None, reader: Optional[Reader] = None) -> None |
| def [`open`](#thirdparty.pparse.lib.BytesExtraction.open)``() -> Reader                                                                                                       |
| def [`tell`](#thirdparty.pparse.lib.BytesExtraction.tell)``() -> int                                                                                                          |
| def [`from_xml`](#thirdparty.pparse.lib.BytesExtraction.from_xml)``(xml_src: Any, pparse_xml: Optional[Any] = None) -> BytesExtraction                                        |
| def [`to_xml`](#thirdparty.pparse.lib.BytesExtraction.to_xml)``() -> str                                                                                                      |

<a id="thirdparty.pparse.lib.Parser"></a>

--------------------------------------------------------------
### Parser
--------------------------------------------------------------

`class Parser()`

#### Attributes

| Attribute       | Default |
| --------------- | ------- |
| _id             | id      |
| _source         | source  |
| current         | None    |
| _all_states     | {}      |
| _base_state_cls | None    |

#### Functions

| Prototype                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.Parser.__init__)``(source: Extraction, id: str, base_state_cls: Optional[Type[Any]] = None) -> None |
| def [`_init_state_as_cls`](#thirdparty.pparse.lib.Parser._init_state_as_cls)``(init_state: Union[str, Type[Any]]) -> Type[Any]              |
| def [`source`](#thirdparty.pparse.lib.Parser.source)``() -> Extraction                                                                      |
| def [`scan_data`](#thirdparty.pparse.lib.Parser.scan_data)``() -> None                                                                      |
| def [`match_extension`](#thirdparty.pparse.lib.Parser.match_extension)``(fname: str) -> bool                                                |
| def [`match_magic`](#thirdparty.pparse.lib.Parser.match_magic)``(cursor: Any) -> bool                                                       |

<a id="thirdparty.pparse.lib.Tensor"></a>

--------------------------------------------------------------
### Tensor
--------------------------------------------------------------

`class Tensor()`

#### Attributes

| Attribute     | Default                                                                                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| STTYPE_STRUCT | {'I8': 'b', 'U8': 'B', 'I16': 'h', 'U16': 'H', 'I32': 'i', 'U32': 'I', 'I64': 'q', 'U64': 'Q', 'F32': 'f', 'F64': 'd'}                                                                   |
| STTYPE_SIZE   | {'I8': 1, 'U8': 1, 'I16': 2, 'U16': 2, 'I32': 4, 'U32': 4, 'I64': 8, 'U64': 8, 'F32': 4, 'F64': 8}                                                                                       |
| STTYPE_NP_MAP | {'F32': numpy.float32, 'F64': numpy.float64, 'F16': numpy.float16, 'I8': numpy.int8, 'I16': numpy.int16, 'I32': numpy.int32, 'I64': numpy.int64, 'U8': numpy.uint8, 'BOOL': numpy.bool_} |

#### Functions

| Prototype                                                                         |
| --------------------------------------------------------------------------------- |
| def [`get_type`](#thirdparty.pparse.lib.Tensor.get_type)``() -> str               |
| def [`get_shape`](#thirdparty.pparse.lib.Tensor.get_shape)``() -> List[int]       |
| def [`get_data_bytes`](#thirdparty.pparse.lib.Tensor.get_data_bytes)``() -> bytes |
| def [`as_array`](#thirdparty.pparse.lib.Tensor.as_array)``() -> Any               |
| def [`as_numpy`](#thirdparty.pparse.lib.Tensor.as_numpy)``() -> numpy.ndarray     |

<a id="thirdparty.pparse.lib.PparseXml"></a>

--------------------------------------------------------------
### PparseXml
--------------------------------------------------------------

`class PparseXml()`

#### Attributes

| Attribute                 | Default |
| ------------------------- | ------- |
| xml                       | xml     |
| _result_ref_to_extraction | {}      |

#### Functions

| Prototype                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------- |
| def [`__init__`](#thirdparty.pparse.lib.PparseXml.__init__)``(xml: Any) -> None                                                    |
| def [`add_result_ref`](#thirdparty.pparse.lib.PparseXml.add_result_ref)``(result_ref_id: int, extraction: BytesExtraction) -> None |
| def [`has_extraction`](#thirdparty.pparse.lib.PparseXml.has_extraction)``(result_ref_id: int) -> bool                              |
| def [`get_extraction`](#thirdparty.pparse.lib.PparseXml.get_extraction)``(result_ref_id: int) -> BytesExtraction                   |
| def [`from_xml`](#thirdparty.pparse.lib.PparseXml.from_xml)``(xml_src: Any) -> PparseXml                                           |
