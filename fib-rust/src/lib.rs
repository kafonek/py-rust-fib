pub fn generate_fibonacci_sequence(n: u32) -> Vec<u32> {
    let mut sequence = Vec::new();
    let mut a = 0;
    let mut b = 1;
    for _ in 0..n {
        sequence.push(a);
        let c = a + b;
        a = b;
        b = c;
    }
    sequence
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_generate_fibonacci_sequence() {
        assert_eq!(generate_fibonacci_sequence(6), vec![0, 1, 1, 2, 3, 5]);
    }
}
