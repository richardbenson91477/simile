.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $main..s0, %rax
    mov %rax, main.s
    mov $1, %rbx
    mov main.s, %rax
    add %rbx, %rax
    mov %rax, main.s
    mov $main..s1, %rdi
    mov main.s, %rsi
    call printf
    pop %rbp
    ret
.section .data
main..s0: .string "Hello, \"world!\""
main.s: .zero 8
main..s1: .string "%s\n"
