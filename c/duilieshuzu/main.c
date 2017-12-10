#include<stdio.h>
#include"duilie.h"
int main(void)
{
	return 0;
}

int IsEmpty(queue q)
{
	return q->size==0;
}

void MakeEmpty(queue q)
{
	q->size=0;
	q->front=1;
	q->rear=0;
}

static int Succ(int value, queue q)
{
	if (++value == q->capacity)
		value=0;
	return value;
}

void Enqueue(int x, queue q)
{
	if(IsFull(q))
		printf("Full queue");
	else
	{
		q->size++;
		q->rear=Succ(q->rear,q);
		q->array[q->rear]=x;
	}
}