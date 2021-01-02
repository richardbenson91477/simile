.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $1, %rax
    mov %rax, main.a
    mov $9, %rbx
    mov main.a, %rax
    add %rbx, %rax
    mov %rax, main.a
    mov $5, %rbx
    mov main.a, %rax
    sub %rbx, %rax
    mov %rax, main.a
    mov $4, %rbx
    mov main.a, %rax
    imul %rbx, %rax
    mov %rax, main.a
    mov $2, %rbx
    mov main.a, %rax
    cltd
    idiv %rbx
    mov %rax, main.a
    mov $main..s0, %rdi
    mov main.a, %rsi
    call printf
    pop %rbp
    ret
.section .data
main.a: .zero 8
main..s0: .string "%d\n"
