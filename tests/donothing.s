.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    pop %rbp
    ret
