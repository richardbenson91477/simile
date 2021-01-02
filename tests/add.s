.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $10, %rdi
    mov $20, %rsi
    call my_add
    mov %rax, main.a
    mov $main..s0, %rdi
    mov main.a, %rsi
    call printf
    pop %rbp
    ret
.section .data
main.a: .zero 8
main..s0: .string "%ld\n"
.section .text
.globl my_add
my_add:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov %rdi, %rbx
    add %rbx, %rax
    mov %rsi, %rbx
    add %rbx, %rax
    pop %rbp
    ret
