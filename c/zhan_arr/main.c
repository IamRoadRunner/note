#include<stdio.h>
#include<stdlib.h>
#include"zhan.h"
int main(void)
{

}
stack CreateStack(int MaxElements)
{
	stack s;
	if(MaxElements<MinStackSize)
		printf("stack is too small");
	s=malloc(sizeof(struct stackrecord));
	if (s==NULL)
		printf("out of space");
	s->array=malloc(sizeof(int)*MaxElements);
	if(s->array==NULL)
		printf("out of space");
	s->capacity=MaxElements;
	MakeEmpty(s);
	return s;
}

void DisposeStack(stack s)
{
	if(s!=NULL)
	{
		free(s->array);
		free(s);
	}
}
int IsEmpty(stack s)
{
	return s->topofstack==EmptyTOS;
}

void MakeEmpty(stack s)
{
	s->topofstack==EmptyTOS;
}

void Push (int x,stack s)
{
	if(IsFull(s))  
		printf("full stack");
	else
		s->array[++s->topofstack]=x;
}

int Top(stack s)
{
	if(!IsEmpty(s))
		return s->array[s->topofstack];
	printf("empty stack");
	return 0;
}

void Pop(stack s)
{
	if(s->topofstack==EmptyTOS)
		printf("Empty stack");
	else
		s->topofstack--;
}

int TopAndPop(stack s)
{
	if(!IsEmpty(s))
		return (s->array[s->topofstack--]);
	printf("empty stack");
	return 0;
}



