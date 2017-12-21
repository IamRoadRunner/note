#include<stdio.h>
#include<stdlib.h>
#include"kaifang.h"
int main(void)
{
	return 0;
}
int NextPrime(int x,int tablesize)
{
	if(x<10)
	{
			if(x%tablesize==0)
				return NextPrime(x,++tablesize);
			else
				return NextPrime(++x,tablesize);
		}
	return tablesize;
}

hashtable InitializeTable(int tablesize)
{
	hashtable h;
	int i;
	if(tablesize < MintableSize)
	{
		printf("tablesize size too small");
		return NULL;
	}
	h=malloc(sizeof(struct hashtbl));
	if (h==NULL)
		printf("out of space");
	h->tablesize=NextPrime(2,tablesize);
	h->thecells=malloc(sizeof(cell)*h->tablesize);
	if (h->thecells==NULL)
		printf("out of space");
	for (i=0;i<h->tablesize;i++)
		h->thecells[i].info=Empty;
	return h;
}

position Find(int key, hashtable h)
{
	position currentpos;
	int collisionnum=0;/*哈西之后的值*/
	currentpos = key%h->tablesize;
	while(h->thecells[currentpos].info!=Empty &&
		h->thecells[currentpos].element!=key)
	{
		currentpos+=2*++collisionnum -1;
		if(currentpos>=h->tablesize)
			currentpos-=h->tablesize;
	}
	return currentpos;
}

void Insert(int key,hashtable h)
{
	position pos;
	pos=Find(key,h);
	if (h->thecells[pos].info!=Legitimate)
	{
		h->thecells[pos].info=Legitimate;
		h->thecells[pos].element=key;
	}
}
