# rustc-bugs

## infinite_recursion
Calling a function that returns an `impl Trait`, and just calls itself in the implementation,
ICE's. This is related to https://github.com/rust-lang/rust/issues/28728 (LLVM optimization bug).

#### Poc
```Rust
fn rec() -> impl Fn() {
    rec()
}

fn main() {
    rec();
}
```

#### Discovery date
2018-07-25

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :white_check_mark:    | :x: |  :x:|

#### issue
https://github.com/rust-lang/rust/issues/52701


## cat_expr Errd
A `& { loop { continue } }` at the place of an array length ICE's

#### Poc
```Rust
fn main() {
    [(); & { loop { continue } } ]
}
```
#### Discovery date
2018-07-16

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :white_check_mark:    | :white_check_mark: |  :x:|

#### issue
https://github.com/rust-lang/rust/issues/52443


## No kind for cast
Casting &(for .... {}) as *const _ as usize as an array length ICE's

#### Poc
```Rust
fn main() {
    fn main() {
    let f = [();  { &loop { break } as *const _ as usize } ];
}
```

#### Discovery date
2018-07-16

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :x:|


#### issue
https://github.com/rust-lang/rust/issues/52442


## Closure expr w/o closure type
Casting &(&'static: loop {closure}) to *const _ to usize as an array length ICE's
Note that this is verry related to the `type of & not region` ICE.

#### PoC
```Rust
fn main() {
    [(); &(&'static: loop { |x| {}; }) as *const _ as usize]
}
```

#### Discovery date
2018-07-16

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :x:|


#### issue
https://github.com/rust-lang/rust/issues/52437


## Expected usize, got Const {...}
Casting a &(static closure) as *const _ as usize as an array length ICE's.
Note that the closure does not have arguments.
This is also verry related to the `type of & not region` ICE, and therefore reported in the same issue.

#### PoC
```Rust
fn main() {
    [(); &(static || {}) as *const _ as usize]
}
```

#### Discovery date
2018-07-16

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :white_check_mark:    | :x: |  :x:|

#### issue
https://github.com/rust-lang/rust/issues/52432


## type of & not region
Casting a &(static closure) as *const _ as usize as an array length ICE's

#### PoC
```Rust
fn main() {
    [(); &(static |x| {}) as *const _ as usize]
}
```

#### Discovery date
2018-07-16

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :x:|


#### issue
https://github.com/rust-lang/rust/issues/52432


## Unexpected type
a `match () { 'c' => 1}` as array length caused an ICE.
Note that this is verry related to the `Returning construct with pattern` ICE, and therefore is reported in the same issue.

#### PoC
```Rust
fn main() {
    [(); return match () {
        'c' => 1,
    }]
}
```

#### Discovery date
2018-07-01

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :white_check_mark:|


#### issue
https://github.com/rust-lang/rust/issues/51963


## Impossible case reached
a `match 1 { 1 => 1}` as array length caused an ICE.
Note that this is verry related to the `Returning construct with pattern` ICE, and therefore is reported in the same issue.

#### PoC
```Rust
fn main() {
    [(); return match 1 {
        1 => 1,
    }]
}
```

#### Discovery date
2018-07-01

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :white_check_mark:|


#### issue
https://github.com/rust-lang/rust/issues/51963


## Returning construct with pattern
Returning anything that has some form of pattern,
like `|x| {}`, or `while let Some(n) = Some(1) {}` in the place of an array-length, causes an ICE.

#### PoC
```Rust
fn main() {
    [(); return | crash | ()];
}
```

#### Alternative PoC
```Rust
fn main() {
    [(); return while Some(n) = Some(1) {}];
}
```

```Rust
fn main() {
    [(); for _ in 0.. {}];
}
```

```Rust
fn main() {
    [(); return match  1 {
        n => n,
    }]
}
```

#### Discovery date
2018-07-01

#### Resolved
| stable | beta | nightly |
| ------ | ---- | ------- |
| :x:    | :x: |  :white_check_mark:|

#### issue
https://github.com/rust-lang/rust/issues/51963


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
| :x:    | :x: |  :white_check_mark: |

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
| :x:    | :x: |  :white_check_mark: |

#### issue
https://github.com/rust-lang/rust/issues/51707


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
