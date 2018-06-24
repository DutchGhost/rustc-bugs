# rustc-bugs

## Break labeled while loop
Breaking a labeled while loop inside of the condiition generated an illigal instruction.

#### PoC
```Rust
fn main() {
    'a: while break 'a {};
}
```

#### Discovery date
2018-05-18

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :white_check_mark: | :white_check_mark: |

#### issue
https://github.com/rust-lang/rust/issues/50856

## Break labeled while loop in constant context
Breaking a labeled while loop inside of a constant context would cause an ICE.

#### PoC
```Rust
fn main() {
    const crash: () = 'a: while break 'a {};
}
```

#### Discovery date
2018-05-30

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: | :x: |

#### issue
https://github.com/rust-lang/rust/issues/51350


## Continue as array length
Writing a `continue` at the place of where the length of an array should go, caused an ICE.

#### PoC
```Rust
fn main() {
    [(); continue]
}
```
#### Discovery date
2018-06-22

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: | :x: |

#### issue
https://github.com/rust-lang/rust/issues/51708


## Break as array length
Writing a `break` at the place of where the length of an array should go, caused an ICE.

#### PoC
```Rust
fn main() {
    loop { |_: [_; break]| {} }
}
```

#### Alternative PoC
```Rust
fn main() {
    loop { [(); break] }
}
```
#### Discovery date
2018-06-22

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: | :x: |

#### issue
https://github.com/rust-lang/rust/issues/51707


## Returing closure
Returning a closure at the place of where the length of an array should go, caused an ICE.

#### PoC
```Rust
fn main() {
    [(); return || {}];
}
```

#### Discovery date
2018-06-22

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :white_check_mark:|

#### issue
https://github.com/rust-lang/rust/issues/51714