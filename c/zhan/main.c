#include<stdio.h>
#include<stdlib.h>
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

void Push (int x, stack s)
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

int Top(stack s)
{
	if(!IsEmpty(s))
		return s->Next->Element;
	Error("Empty stack");
	return 0;
}

void Pop(stack s)
{
	ptrtonode firstcell;
	if (IsEmpty(s))
		Error("Empty stack");
	else
	{
		firstcell = s->Next;
		s->Next = s->Next->Next;
		free(firstcell);
	}
}
