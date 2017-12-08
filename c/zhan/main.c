#include<stdio.h>
#include "zhan.h"

int main(void)
{
	return 0;
}
int IsEmpty(stack s)
{
	return s->Next == NULL;
}

stack CreateStack(void)
{
	stack s;
	s = malloc(sizeof(struct Node));
	if (s==NULL)
		FatalError("out of space");
	s->Next==NULL;
	MakeEmpty(s);
	return s;
}
void MakeEmpty(stack s)
{
	if(s==NULL)
		Error("usr CreateStack first");
	else
		while(!IsEmpty(s))
			Pop(s);
}

void Push (ElementType x, stack s)
{
	ptrtonode tmpcell;
	tmpcell = malloc(sizeof(struct Node));
	if(tmpcell==NULL)
		FatalError("out of space");
	else
	{
		tmpcell->Element = x;
		tmpcell->Next=s->Next;
		s->Next=tmpcell;
	}
}
