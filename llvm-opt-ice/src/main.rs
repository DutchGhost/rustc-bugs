
fn rec() -> impl Fn() { rec() }

fn main() {
    let f = rec();
}