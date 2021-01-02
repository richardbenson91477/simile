.section .text
.globl main
main:
    push %rbp
    mov %rsp, %rbp
    xor %rax, %rax
    mov $0, %rax
    mov %rax, main.x
    mov $1, %rax
    mov %rax, main.y
    mov $1, %rax
    mov %rax, main.z
    mov main.x, %rax
    test %rax, %rax
    jz main.else.0
    mov $main..s0, %rdi
    call puts
    mov main.y, %rax
    test %rax, %rax
    jz main.else.1
    mov $main..s1, %rdi
    call puts
    jmp main.endif.1
main.else.1:
    mov $main..s2, %rdi
    call puts
main.endif.1:
    jmp main.endif.0
main.else.0:
    mov $main..s3, %rdi
    call puts
    mov main.z, %rax
    test %rax, %rax
    jz main.else.2
    mov $main..s4, %rdi
    call puts
    jmp main.endif.2
main.else.2:
    mov $main..s5, %rdi
    call puts
main.endif.2:
main.endif.0:
    pop %rbp
    ret
.section .data
main.x: .zero 8
main.y: .zero 8
main.z: .zero 8
main..s0: .string "x is nonzero"
main..s1: .string "y is nonzero"
main..s2: .string "y is zero"
main..s3: .string "x is zero"
main..s4: .string "z is nonzero"
main..s5: .string "z is zero"
