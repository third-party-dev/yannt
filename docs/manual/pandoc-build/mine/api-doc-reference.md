---
title: "MyLibrary API Reference"
subtitle: "Core Networking Module"
version: "2.1.0"
author: "MyLibrary Contributors"
date: "2025"
toc: true
---

<!-- ═══════════════════════════════════════════════════════════════════════════
     PATTERNS USED IN THIS FILE
     ───────────────────────────────────────────────────────────────────────
     Namespace separator : <div class="namespace-rule" id="fqn"></div>
     Namespace anchor    : <a id="fqn"></a>  (own paragraph, before heading)
     Namespace heading   : # ShortName       (standard Markdown, appears in TOC)
     Qualified name      : <small>`fqn`</small>

     Member separator    : <div class="member-rule"></div>
     Member anchor+name  : <div class="member-name" id="fqn"><code>name</code></div>
     Member qual. name   : <small>`fqn`</small>

     Summary tables      : Pandoc simple_tables (readable, no | column clashes)
                           Column alignment set by header underline length.
                           Pipe tables also accepted by the Lua filter.
                           Both formats produce identical Pandoc Table AST nodes.

     Docstring sections  : **Bold label** followed by unordered list.
     Declarations        : ```python fenced block labelled **Declaration**
     Internal links      : [text](#fqn)  — standard Markdown, no {#} notation
═══════════════════════════════════════════════════════════════════════════ -->


<!-- ═══════════════════════════════════════════════════════════════════════════
     GLOBAL NAMESPACE: mylib.network
═══════════════════════════════════════════════════════════════════════════ -->


<div class="namespace-rule" id="mylib.network"></div>

<a id="mylib.network"></a>

# network

<small>`mylib.network`</small>

Core networking utilities for connection management, retry logic, and data
transport. This module provides the foundational layer for all client-server
communication within MyLibrary.

---

**Attributes**

Name                                                   Type     Default   Description
-----------------------------------------------------  -------  --------  -----------------------------------------
[`DEFAULT_TIMEOUT`](#mylib.network.DEFAULT_TIMEOUT)    `float`  `30.0`    Global socket timeout in seconds.
[`MAX_POOL_SIZE`](#mylib.network.MAX_POOL_SIZE)        `int`    `10`      Maximum concurrent connections in pool.
[`RETRY_BACKOFF`](#mylib.network.RETRY_BACKOFF)        `float`  `1.5`     Exponential backoff multiplier for retries.

**Functions**

Name                                                    Description
------------------------------------------------------  -------------------------------------------------------
[`connect()`](#mylib.network.connect)                   Open a managed connection to a remote host.
[`ping()`](#mylib.network.ping)                         Check reachability without opening a session.
[`get_pool_stats()`](#mylib.network.get_pool_stats)     Return current connection pool metrics.

---

<!-- ─── Attribute: DEFAULT_TIMEOUT ─────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.DEFAULT_TIMEOUT"><code>DEFAULT_TIMEOUT</code></div>

<small>`mylib.network.DEFAULT_TIMEOUT`</small>

Global default socket timeout applied to all new connections unless
overridden at call-site.

**Type:** `float`  
**Default:** `30.0`

<!-- ─── Attribute: MAX_POOL_SIZE ───────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.MAX_POOL_SIZE"><code>MAX_POOL_SIZE</code></div>

<small>`mylib.network.MAX_POOL_SIZE`</small>

Upper bound on simultaneous connections held in the internal pool. Requests
beyond this limit block until a slot becomes available.

**Type:** `int`  
**Default:** `10`

<!-- ─── Attribute: RETRY_BACKOFF ───────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.RETRY_BACKOFF"><code>RETRY_BACKOFF</code></div>

<small>`mylib.network.RETRY_BACKOFF`</small>

Multiplier applied to the base delay on each successive retry attempt.
A value of `1.5` with a 1-second base yields delays of 1 s, 1.5 s, 2.25 s…

**Type:** `float`  
**Default:** `1.5`

<!-- ─── Function: connect ──────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.connect"><code>connect</code></div>

<small>`mylib.network.connect`</small>

Open a managed connection to a remote host, respecting the module-level
retry policy and connection pool constraints.

Connections returned by this function are tracked in the internal pool and
must be released via [`Connection.close()`](#mylib.network.Connection.close)
or used as a context manager to avoid pool exhaustion.

**Declaration**

```python
def connect(
    host: str,
    port: int = 443,
    *,
    timeout: float | None = None,
    ssl: bool = True,
    retries: int = 3,
) -> "Connection":
```

**Parameters**

- **`host`** (`str`) — Hostname or IP address of the target server.
- **`port`** (`int`, default `443`) — TCP port to connect on.
- **`timeout`** (`float | None`, default `None`) — Per-operation socket
  timeout in seconds. `None` inherits `DEFAULT_TIMEOUT`.
- **`ssl`** (`bool`, default `True`) — Whether to wrap the socket in TLS.
- **`retries`** (`int`, default `3`) — Maximum connection attempts before
  raising `ConnectionError`.

**Returns**

- `Connection` — An active, pool-tracked connection object ready for use.

**Raises**

- `ConnectionError` — If the host is unreachable after all retry attempts.
- `SSLError` — If TLS negotiation fails and `ssl=True`.
- `ValueError` — If `port` is not in the range 1–65535.

**See Also**

- [`Connection`](#mylib.network.Connection) — The returned connection type.
- [`get_pool_stats()`](#mylib.network.get_pool_stats) — Inspect current pool usage.

<!-- ─── Function: ping ─────────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.ping"><code>ping</code></div>

<small>`mylib.network.ping`</small>

Check whether a host is reachable without establishing a full session.
Uses a lightweight TCP handshake and does not consume a pool slot.

**Declaration**

```python
def ping(host: str, port: int = 443, *, timeout: float = 5.0) -> bool:
```

**Parameters**

- **`host`** (`str`) — Hostname or IP address to probe.
- **`port`** (`int`, default `443`) — Port to probe on.
- **`timeout`** (`float`, default `5.0`) — Maximum wait in seconds.

**Returns**

- `bool` — `True` if the host accepted the TCP handshake, `False` otherwise.

<!-- ─── Function: get_pool_stats ───────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.get_pool_stats"><code>get_pool_stats</code></div>

<small>`mylib.network.get_pool_stats`</small>

Return a snapshot of the current connection pool state.

**Declaration**

```python
def get_pool_stats() -> dict[str, int]:
```

**Returns**

- `dict[str, int]` — Mapping with keys `active`, `idle`, `waiting`
  reflecting pool slot counts at the moment of the call.


<!-- ═══════════════════════════════════════════════════════════════════════════
     CLASS NAMESPACE: Connection
     -----------------------------------------------------------------------
     Class namespaces follow the same pattern as module namespaces.
     The __init__ docstring renders directly under the class heading.
     No separate __init__ entry appears in the member listing below.
═══════════════════════════════════════════════════════════════════════════ -->

<div class="pagegroup">

<div class="namespace-rule" id="mylib.network.Connection"></div>

<a id="mylib.network.Connection"></a>

# Connection

<small>`mylib.network.Connection`</small>

A managed, pool-tracked connection to a remote host.

Wraps a raw socket with retry logic, TLS negotiation, and automatic pool
registration. Instances should be obtained via
[`connect()`](#mylib.network.connect) rather than instantiated directly.
Supports the context manager protocol for automatic cleanup.

**Declaration**

```python
class Connection(AbstractConnection):
    def __init__(
        self,
        host: str,
        port: int,
        *,
        ssl: bool = True,
        timeout: float | None = None,
    ):
```

**Parameters**

- **`host`** (`str`) — Remote hostname or IP.
- **`port`** (`int`) — Remote TCP port.
- **`ssl`** (`bool`, default `True`) — Enable TLS.
- **`timeout`** (`float | None`, default `None`) — Socket timeout; `None`
  uses `DEFAULT_TIMEOUT`.

**Raises**

- `ConnectionError` — If the initial handshake fails.

---

<div class="pagegroup">

**Attributes**

Name                                                        Type     Description
----------------------------------------------------------  -------  --------------------------------------------
[`host`](#mylib.network.Connection.host)                    `str`    The remote hostname.
[`port`](#mylib.network.Connection.port)                    `int`    The remote port.
[`is_open`](#mylib.network.Connection.is_open)              `bool`   Whether the connection is currently active.
[`bytes_sent`](#mylib.network.Connection.bytes_sent)        `int`    Cumulative bytes written on this connection.
[`bytes_received`](#mylib.network.Connection.bytes_received) `int`   Cumulative bytes read on this connection.

</div>

<div class="pagegroup">

**Methods**

Name                                                        Description
----------------------------------------------------------  -----------------------------------------------
[`send()`](#mylib.network.Connection.send)                  Write bytes to the connection.
[`receive()`](#mylib.network.Connection.receive)            Read bytes from the connection.
[`stream()`](#mylib.network.Connection.stream)              Iterate over chunks of incoming data.
[`close()`](#mylib.network.Connection.close)                Release the connection back to the pool.

</div>

---

<!-- ─── Attribute: host ────────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.host"><code>host</code></div>

<small>`mylib.network.Connection.host`</small>

The remote hostname or IP address this connection targets. Read-only after
construction.

**Type:** `str`

<!-- ─── Attribute: is_open ─────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.is_open"><code>is_open</code></div>

<small>`mylib.network.Connection.is_open`</small>

`True` if the underlying socket is connected and the TLS handshake (if
applicable) has completed successfully. Set to `False` by `close()` or
any unrecoverable socket error.

**Type:** `bool`

<!-- ─── Method: send ───────────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.send"><code>send</code></div>

<small>`mylib.network.Connection.send`</small>

Write a byte buffer to the remote peer. Blocks until all data is handed
to the OS send buffer.

**Declaration**

```python
def send(self, data: bytes, *, flags: int = 0) -> int:
```

**Parameters**

- **`data`** (`bytes`) — Payload to transmit.
- **`flags`** (`int`, default `0`) — Low-level socket flags passed
  directly to `socket.send()`.

**Returns**

- `int` — Number of bytes actually enqueued in the OS send buffer.

**Raises**

- `ConnectionError` — If the connection has been closed.
- `OSError` — On underlying socket errors.

<!-- ─── Method: receive ────────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.receive"><code>receive</code></div>

<small>`mylib.network.Connection.receive`</small>

Read up to `size` bytes from the remote peer. Blocks until at least one
byte is available or the timeout expires.

**Declaration**

```python
def receive(self, size: int = 4096) -> bytes:
```

**Parameters**

- **`size`** (`int`, default `4096`) — Maximum bytes to read in a single
  call.

**Returns**

- `bytes` — Data received; may be shorter than `size`. An empty `bytes`
  object signals the peer closed the connection.

**Raises**

- `TimeoutError` — If no data arrives within the configured timeout.
- `ConnectionError` — If the connection has been closed.

<!-- ─── Method: stream ─────────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.stream"><code>stream</code></div>

<small>`mylib.network.Connection.stream`</small>

Iterate over successive chunks of incoming data until the remote peer
closes the connection or the timeout elapses.

Useful for consuming large or indefinitely long responses without
buffering the entire payload in memory.

**Declaration**

```python
def stream(
    self,
    chunk_size: int = 4096,
    *,
    timeout: float | None = None,
) -> Iterator[bytes]:
```

**Parameters**

- **`chunk_size`** (`int`, default `4096`) — Maximum bytes per yielded chunk.
- **`timeout`** (`float | None`, default `None`) — Per-chunk read timeout.
  `None` inherits the connection's configured timeout.

**Yields**

- `bytes` — One chunk of received data per iteration. Never empty; the
  iterator ends when the peer closes the connection.

**Raises**

- `TimeoutError` — If a chunk does not arrive within the per-chunk timeout.
- `ConnectionError` — If the connection drops mid-stream.

<!-- ─── Method: close ──────────────────────────────────────────────────── -->

<div class="pagegroup">

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.Connection.close"><code>close</code></div>

<small>`mylib.network.Connection.close`</small>

Gracefully shut down the connection and return its slot to the pool.
Safe to call multiple times; subsequent calls are no-ops.

**Declaration**

```python
def close(self, *, force: bool = False) -> None:
```

**Parameters**

- **`force`** (`bool`, default `False`) — If `True`, performs an abortive
  reset (`RST`) instead of a graceful `FIN` sequence. Use only when the
  peer is known to be unresponsive.

**Returns**

- `None`


</div><!-- connection.close pagegroup -->

</div><!-- connection pagegroup -->

<!-- ═══════════════════════════════════════════════════════════════════════════
     CLASS NAMESPACE: RetryPolicy
═══════════════════════════════════════════════════════════════════════════ -->

<div class="pagebreak"></div>
<div class="namespace-rule" id="mylib.network.RetryPolicy"></div>

<a id="mylib.network.RetryPolicy"></a>

<div class="h1-style">RetryPolicy</div>

<small>`mylib.network.RetryPolicy`</small>

Immutable value object describing how connection and send failures should
be retried.

Pass an instance to [`connect()`](#mylib.network.connect) via the
`retry_policy` keyword argument to override module-level defaults on a
per-connection basis.

**Declaration**

```python
@dataclass(frozen=True)
class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        backoff: float = 1.5,
        jitter: bool = True,
        retry_on: tuple[type[Exception], ...] = (ConnectionError, TimeoutError),
    ):
```

**Parameters**

- **`max_attempts`** (`int`, default `3`) — Total number of tries,
  including the first attempt.
- **`base_delay`** (`float`, default `1.0`) — Initial wait in seconds
  before the first retry.
- **`backoff`** (`float`, default `1.5`) — Multiplier applied to the delay
  after each failed attempt.
- **`jitter`** (`bool`, default `True`) — If `True`, adds a small random
  offset to each delay to avoid thundering-herd patterns.
- **`retry_on`** (`tuple[type[Exception], ...]`) — Exception types that
  trigger a retry; all others propagate immediately.

---

**Attributes**

Name                                                           Type     Default   Description
-------------------------------------------------------------  -------  --------  ---------------------------------
[`max_attempts`](#mylib.network.RetryPolicy.max_attempts)      `int`    `3`       Total attempts including first.
[`base_delay`](#mylib.network.RetryPolicy.base_delay)          `float`  `1.0`     Initial delay in seconds.
[`backoff`](#mylib.network.RetryPolicy.backoff)                `float`  `1.5`     Exponential backoff multiplier.
[`jitter`](#mylib.network.RetryPolicy.jitter)                  `bool`   `True`    Randomise delay offsets.

---

<!-- ─── Attribute: max_attempts ───────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.RetryPolicy.max_attempts"><code>max_attempts</code></div>

<small>`mylib.network.RetryPolicy.max_attempts`</small>

Total number of attempts, counting the first. A value of `1` means no
retries; a value of `3` means one initial attempt plus two retries.

**Type:** `int`  
**Default:** `3`

<!-- ─── Attribute: backoff ─────────────────────────────────────────────── -->

<div class="member-rule"></div>

<div class="member-name" id="mylib.network.RetryPolicy.backoff"><code>backoff</code></div>

<small>`mylib.network.RetryPolicy.backoff`</small>

Exponential multiplier applied to `base_delay` between retries.
Effective delays: `base_delay`, `base_delay × backoff`,
`base_delay × backoff²`, …

**Type:** `float`  
**Default:** `1.5`
