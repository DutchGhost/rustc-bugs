# rustc-bugs

## Break labeled while loop

Breaking a labeled while loop inside of the condiition generated an illigal instruction

### PoC

```Rust
'a: while break 'a {};
```

### issue
https://github.com/rust-lang/rust/issues/50856

