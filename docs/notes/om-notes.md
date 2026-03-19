starts with `IMOD`

```c
struct ModelHeader {
    char magic[4];        // usually "IMOD" or similar
    uint32_t version;
    uint32_t header_size;

    uint32_t partition_count;
    uint64_t partition_table_offset;

    uint64_t model_size;

    uint8_t reserved[...];
};

/*
Partition Types:
0	MODEL_DEF (graph)
1	WEIGHTS
2	TASK_INFO
3	TBE_KERNELS
4	AI_CPU
5	MEMORY
6	ATTR
7	OP_DEBUG
8	RESERVED
*/

/*
MODEL_DEF (graph)

GraphDef
 ├── Nodes
 │    ├── op_type
 │    ├── inputs
 │    ├── outputs
 │    ├── attributes
 ├── TensorDesc
 ├── Edge info

field_key = (field_number << 3) | wire_type

Wire Types:
0	varint
1	64-bit
2	length-delimited
5	32-bit

WEIGHTS

[offset table?] (sometimes)
[data blobs]

TBE_KERNELS

Compiled kernels (maybe ELF-like)

TASK_INFO

Scheduling


*/

struct PartitionEntry {
    uint32_t type;        // enum
    uint32_t offset;      // from file start
    uint32_t size;
    uint32_t flags;       // often 0
};

```

```python
import struct

def read_header(data):
    magic = data[0:4]
    version, header_size, part_count = struct.unpack_from("<III", data, 4)
    part_offset = struct.unpack_from("<Q", data, 16)[0]

    return {
        "magic": magic,
        "version": version,
        "header_size": header_size,
        "part_count": part_count,
        "part_offset": part_offset,
    }


def read_partitions(data, offset, count):
    parts = []
    for i in range(count):
        base = offset + i * 16
        p_type, p_off, p_size, flags = struct.unpack_from("<IIII", data, base)
        parts.append({
            "type": p_type,
            "offset": p_off,
            "size": p_size,
            "flags": flags
        })
    return parts

def read_varint(data, offset):
    result = 0
    shift = 0

    while True:
        b = data[offset]
        offset += 1

        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break

        shift += 7

    return result, offset

def parse_fields(data, start, end):
    offset = start
    fields = []

    while offset < end:
        key, offset = read_varint(data, offset)

        field_num = key >> 3
        wire_type = key & 0x7

        if wire_type == 0:  # varint
            val, offset = read_varint(data, offset)

        elif wire_type == 1:  # 64-bit
            val = data[offset:offset+8]
            offset += 8

        elif wire_type == 2:  # length-delimited
            length, offset = read_varint(data, offset)
            val = data[offset:offset+length]
            offset += length

        elif wire_type == 5:  # 32-bit
            val = data[offset:offset+4]
            offset += 4

        else:
            raise ValueError(f"Unknown wire type {wire_type}")

        fields.append((field_num, wire_type, val))

    return fields

def get_partition(data, parts, ptype):
    for p in parts:
        if p["type"] == ptype:
            return data[p["offset"]:p["offset"] + p["size"]]
    return None

def decode_graph():
    model_def = get_partition(data, parts, 0)

    fields = parse_fields(model_def, 0, len(model_def))

    for f in fields[:50]:
        print(f[0], f[1], len(f[2]) if isinstance(f[2], bytes) else f[2])
```


```
Offset  Size  Type    Value            Interpretation
------  ----  ------  ---------------  ------------------------------------------
0x00     8    u64     640              Block size (0x280 — covers this sub-header
                                       plus the graph index that follows at 0x70)
0x08     4    u32     1                num_sections (always 1 per graph)
0x0c     4    u32     112 (0x70)       inner_header_size — protobuf starts at
                                       this offset from 0x00, i.e. file offset +0x70
0x10     4    u32     1                num_graphs
0x14     4    u32     2,822,400        graph_memory_size — runtime heap needed to
                                       expand the graph (not the serialised size)
0x18     4    u32     0                reserved
0x1c     4    u32     2                num_output_dims (C=84, HW=8400 → 2 values)

--- output tensor descriptor (32 bytes) ---
0x20     4    u32     0                output index
0x24     4    u32     28               output name length
0x28     4    u32     24               aligned name field size (padded to 8)
0x2c     4    u32     24               (same — likely offset within this block)
0x30     4    u32     0                padding
0x34    28    char[]  "/model.24/Concat_3:0:output0"   output tensor name

--- output shape descriptor (repeated twice: input side / output side) ---
0x50     8    u64     1                batch size
0x58     8    u64     84               C dimension  (80 classes + 4 bbox)
0x60     8    u64     8400             HW dimension (80²+40²+20² anchor points)
0x68     8    u64     1                batch size   (repeated)
0x70     8    u64     84               C            (repeated)
0x78     8    u64     8400             HW           (repeated)
```