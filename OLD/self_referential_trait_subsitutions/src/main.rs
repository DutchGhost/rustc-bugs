fn test_impl_Add() -> impl std::ops::Add {1 + 1}
fn test_impl_Sub() -> impl std::ops::Sub {1 - 1}
fn test_impl_Mul() -> impl std::ops::Mul {1 * 1}
fn test_impl_Div() -> impl std::ops::Div {2 / 1}

fn test_impl_AddAssign() -> impl std::ops::AddAssign { 1 }
fn test_impl_SubAssign() -> impl std::ops::SubAssign { 1 }
fn test_impl_MulAssign() -> impl std::ops::MulAssign { 1 }
fn test_impl_DivAssign() -> impl std::ops::DivAssign { 1 }

fn main() {
    
}