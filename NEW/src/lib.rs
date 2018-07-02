#![cfg_attr(feature = "generator_ice", feature(generator_trait, generators))]

/// In this module are a number of ICE's defined. Each ICE is identified by the message the ICE
/// gives. Furthermore, the versions in which the piece of code ICE's is also specified.
///
/// To test all ICE's, run `python check.py`. It will read Cargo.toml, grab all the info it needs,
/// and start compiling. Whenever a function ICE's, the backtrace will be written to
/// \backtrace\<icename>\<version>.
pub mod internal_compiler_errors {
    /// Returning any construct with a pattern as an array length ICE's
    ///  # Examples
    /// ```
    /// [(); return | crash | ()]
    /// ```
    #[cfg(all(feature = "missing_binding_mode", any(feature = "stable", feature = "beta", feature = "nightly")))]
    pub fn missing_binding_mode() {
        [(); return | crash | ()]
    }
    
    /// Returning a match that does not cover all patterns as an array length ICE's
    /// # Examples
    /// ```
    /// [(); return match 1 {
    ///     1 => 1,
    /// }]
    /// ```
    #[cfg(all(feature = "impossible_case_reached", any(feature = "stable", feature = "beta", feature = "nightly")))]
    pub fn impossible_case_reached() {
        [(); return match 1 {
            1 => 1,
        }]
    }
    

    /// Returning a match that matches on wrong types as an array length ICE's.
    /// # Examples
    /// ```
    /// [() return match () {
    ///     'c' => 1,
    /// }]
    /// ```
    #[cfg(all(feature = "unexpected_type", any(feature = "stable", feature = "beta", feature = "nightly")))]
    pub fn unexpected_type() {
        [(); return match () {
            'c' => 1,
        }]
    }
    
    /// Returning a closure without arguments as an array length ICE's.
    /// # Examples
    /// ```
    /// [(); return || {}]
    /// ```
    #[cfg(all(feature = "closure_expr_node_id", any(feature = "stable", feature = "beta")))]
    pub fn closure_expr_node_id() {
        [(); return || {}]
    }
    
    /// Putting a `break` as an array length ICE's.
    /// # Examples
    /// ```
    /// while |_: [_; break]| {} {}
    /// ```
    #[cfg(all(feature = "assertion_failed", any(feature = "stable", feature = "beta")))]
    pub fn assertion_failed() {
        while |_: [_; break] | {} {}
    }

    /// Putting a `continue` as an array length ICE's.
    /// # Examples
    /// ```
    /// while |_: [_; continue] | {} {}
    /// ```
    #[cfg(all(feature = "invalid_loop_id", any(feature = "stable", feature = "beta")))]
    pub fn invalid_loop_id() {
        while |_: [_; continue] | {} {}
    }

    /// Breaking a labeled loop in a constant context ICE's
    /// # Examples
    /// ```
    /// const crash: () = 'a: while break 'a {};
    /// ```
    #[cfg(all(feature = "multiple_assignments", any(feature = "stable", feature = "beta", feature = "nightly")))]
    pub fn multiple_assignments() {
        const crash: () = 'a: while break 'a {};
    }

    /// Calling a macro that advances a generator, with a generator that is not bound to a
    /// variable, ICE's.
    #[cfg(all(feature = "broken_mir", feature = "generator_ice", any(feature = "nightly")))] 
    pub fn broken_mir() {
        use std::ops::{Generator, GeneratorState};

        macro_rules! yield_from {
            ($generator:expr) => (
                unsafe {
                    loop {
                        match $generator.resume() {
                            GeneratorState::Yielded(y) => yield y,
                            GeneratorState::Complete(ret) => break ret,
                        }
                    }
                }
            );
        }

        || {
            yield_from!(|| {
                yield;
            });
            return;
        };
    }
}

pub mod invalid_code_generation {
    /// Breaking a labeled while loop generated an executable with a ud2 instruction
    /// # Examples
    /// ```
    /// 'a: while break 'a {};
    /// ```
    #[cfg(all(feature = "break_labeled_while", any(feature = "stable")))]
    pub fn break_labeled_loop() {
        'a: while break 'a {}
    }
}

#[cfg(test)]
mod tests {
    
    #[cfg(all(feature = "break_labeled_while", any(feature = "stable")))]
    #[test]
    fn test_break_labeled_loop() {
        use invalid_code_generation::break_labeled_loop;

        break_labeled_loop();
    }
}
