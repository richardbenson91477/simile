.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $9, %rbx
    add %rbx, %rax
    mov $1, %rbx
    add %rbx, %rax
    mov $5, %rbx
    sub %rbx, %rax
    mov $4, %rbx
    imul %rbx, %rax
    mov $2, %rbx
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
