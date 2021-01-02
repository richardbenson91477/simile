.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $main..s0, %rdi
    mov $main..s1, %rsi
    call printf
    pop %rbp
    ret
.section .data
main..s0: .string "%s\n"
main..s1: .string "Hello, world!"
