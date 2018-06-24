# rustc-bugs

| Name | Description |          PoC          | Discovery Date | Issue |
| -----| ------------| --------------------- | -------------- | ----- |
| Break labeled while loop| Breaking inside of the condition of a while loop caused an ICE | ```Rust
'a: while break 'a {};
``` | 2018-05-18 | https://github.com/rust-lang/rust/issues/50856 |
