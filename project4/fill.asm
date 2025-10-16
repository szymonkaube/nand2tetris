(LOOP)

// i = 0
@i
M=0

// if key is not pressed go to WHITE
@KBD
D=M
@WHTLOOP
D;JEQ

// if key is pressed

// while i < 8192
(BLKLOOP)

// RAM[SCREEN + i] = -1
@SCREEN
D=A
@i
A=D+M
M=-1

// i = i + 1
@8192
D=A
@i
M=M+1
D=M-D

@BLKLOOP
D;JLT

// if key is pressed go to LOOP (start)
@KBD
D=M
@LOOP
D;JNE

(WHTLOOP)

// RAM[SCREEN + i] = -1
@SCREEN
D=A
@i
A=D+M
M=0

// i = i + 1
@8192
D=A
@i
M=M+1
D=M-D

@WHTLOOP
D;JLT


@LOOP
0;JMP
