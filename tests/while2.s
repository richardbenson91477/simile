.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $10, %rax
    mov %rax, main.i
main.while.0:
    mov main.i, %rax
    test %rax, %rax
    jz main.wend.0
    mov main.i, %rax
    mov %rax, main.a
    mov $64, %rbx
    mov main.a, %rax
    add %rbx, %rax
    mov %rax, main.a
    mov main.a, %rdi
    call putchar
    mov $' ', %rdi
    call putchar
    mov $10, %rax
    mov %rax, main.j
main.while.1:
    mov main.j, %rax
    test %rax, %rax
    jz main.wend.1
    mov main.j, %rax
    mov %rax, main.a
    mov $64, %rbx
    mov main.a, %rax
    add %rbx, %rax
    mov %rax, main.a
    mov main.a, %rdi
    call putchar
    mov $1, %rbx
    mov main.j, %rax
    sub %rbx, %rax
    mov %rax, main.j
    jmp main.while.1
main.wend.1:
    mov $'\n', %rdi
    call putchar
    mov $1, %rbx
    mov main.i, %rax
    sub %rbx, %rax
    mov %rax, main.i
    jmp main.while.0
main.wend.0:
    mov $'\n', %rdi
    call putchar
    pop %rbp
    ret
.section .data
main.i: .zero 8
main.a: .zero 8
main.j: .zero 8
