# rustc-bugs

## Break labeled while loop

Breaking a labeled while loop inside of the condiition generated an illigal instruction

##### PoC

```Rust
'a: while break 'a {};
```

##### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :white_check_maker: | :white_check_mark:

##### issue
https://github.com/rust-lang/rust/issues/50856




 :white_check_mark:
  :x:
