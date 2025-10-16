// set a=R0
@R0
D=M
@a
M=D

// set b=R1
@R1
D=M
@b
M=D

// set i=1
@i
M=1

// set result=0
@result
M=0

(LOOP)
  // leave loop if i > n
  @i
  D=M
  @b
  D=D-M
  @END
  D;JGT

  // set result = result + a
  @a
  D=M
  @result
  M=D+M

  @i
  M=M+1

  @LOOP
  0;JMP


(END)
  // set R2 = result
  @result
  D=M
  @R2
  M=D

  @END
  0;JMP
