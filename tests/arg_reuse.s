.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $20, %rdi
    call test
    pop %rbp
    ret
.section .text
.globl test
test:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov %rdi, %rax
    mov %rax, test.a
    mov $test..s0, %rdi
    mov test.a, %rsi
    call printf
    pop %rsp
    ret
.section .data
test.a: .zero 8
test..s0: .string "%d\n"
