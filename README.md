# BrainScript

Brainscript is a variant of Brainfuck inspired by modern programming languages like JavaScript or C++. The interpreter is written in Python. This variant contains a function system allowing you to make function calls in your code.

## Quick Start

### First code
When your code starts, the interpreter will directly call the main function. Your code must look like this at the first place :
```
absolute:main {;
  add(97);
  print(10);
};
```
_The following code prints the character 'a' 10 times._

### Methods
Every Brainfuck instruction has their method in BrainScript.

BrainScript | Brainfuck
------------|-----------
add(num); | +
sub(num); | -
right(num); | >
left(num); | <
print(num); | .
input(); | ,
!; | \[
?; | \]

The _num_ in the methods is the amount of time that the instruction is gonna be repeated.
- add(5); will be +++++
- left(); will be <
- right(3); will be >>>

### Functions

They will allow you to not repeat lines of code over and over. To make functions, you just simply have to do that :
```
absolute:AbsoluteFunction {;
  (code)
  To make a function called "absolute"
 };
 
 relative:RelativeFunction {;
  (code)
  To make a function called "relative"
};
```

The functions can be then called this way : `FunctionName();`

### What is those relative/absolute stuff?

- When a function is called "relative", that means the function will start operating with the data pointer on it's current position.

- When a function is called "absolute", that means the function will start operating with the data pointer on the position 0

However, once the function called, the data pointer will get back at it's position when the function has been called.

## Using it

1. Clone the repository
2. If it has been downloaded as ZIP, extract it
3. Write code in a file
4. Run main.py in a command prompt/terminal with the filename as command line argument

### Is there examples?

Yes.
