use num_bigint::BigInt;
use num_traits::{One, Zero};
use std::mem::replace;

// https://docs.rs/num-bigint/latest/num_bigint/#example
// Return the nth Fibonacci number
pub fn fib(n: u32) -> BigInt {
    let mut a = BigInt::zero();
    let mut b = BigInt::one();
    for _ in 0..n {
        let tmp = a + &b;
        a = replace(&mut b, tmp);
    }
    a
}

#[cfg(test)]
mod tests {
    use super::*;
    // test fib 1-5, fib 10, fib 100
    #[test]
    fn test_fib() {
        assert_eq!(fib(1), BigInt::from(1u32));
        assert_eq!(fib(2), BigInt::from(1u32));
        assert_eq!(fib(3), BigInt::from(2u32));
        assert_eq!(fib(4), BigInt::from(3u32));
        assert_eq!(fib(5), BigInt::from(5u32));
        assert_eq!(fib(10), BigInt::from(55u32));
        assert_eq!(
            fib(100),
            BigInt::parse_bytes(b"354224848179261915075", 10).unwrap()
        );
    }
}
