.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $'a', %rax
    mov %rax, main.c
    mov $26, %rax
    mov %rax, main.x
main.while.0:
    mov main.x, %rax
    test %rax, %rax
    jz main.wend.0
    mov main.c, %rdi
    call putchar
    mov $1, %rbx
    mov main.c, %rax
    add %rbx, %rax
    mov %rax, main.c
    mov $1, %rbx
    mov main.x, %rax
    sub %rbx, %rax
    mov %rax, main.x
    jmp main.while.0
main.wend.0:
    mov $'\n', %rdi
    call putchar
    pop %rbp
    ret
.section .data
main.c: .zero 8
main.x: .zero 8
