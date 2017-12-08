#ifndef _Stack_h
struct stackrecord;
typedef struct stackrecord *stack;

int IsEmpty(stack s);
int IsFull(stack s);
stack CreateStack(int MaxElements);
void DisposeStack(stack s);
void MakeEmpty(stack s);
void Push(int x, stack s);
int Top(stack s);
void Pop(stack s);
int TopAndPop(stack s);
#endif
#define EmptyTOS (-1)
#define MinStackSize  (5)
struct stackrecord
{
	int capacity;
	int topofstack;
	int *array;

};
