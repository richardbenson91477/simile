.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $main..l0, %rax
    mov %rax, main.a
    mov main.a, %rax
    mov %rax, main.b
    mov $33333, %rax
    mov main.b, %r10
    mov %rax, (%r10)
    mov $8, %rbx
    mov main.b, %rax
    add %rbx, %rax
    mov %rax, main.b
    mov $5555, %rax
    mov main.b, %r10
    mov %rax, (%r10)
    mov $main..s0, %rdi
    mov main.a, %rsi
    mov (%rsi), %rsi
    mov main.b, %rdx
    mov (%rdx), %rdx
    call printf
    pop %rbp
    ret
.section .data
main..l0: .zero 16
main.a: .zero 8
main.b: .zero 8
main..s0: .string "%ld %ld\n"
