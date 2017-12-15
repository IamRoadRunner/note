#include<stdio.h>
#include<stdlib.h>
#include"fenli.h"
int main(void)
{
	return 0;
}
Index Hash(int key, int tablesize)
{
	return key%tablesize;
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

hashtable Initializetable(int tablesize)
{
	hashtable h;
	if(tablesize<mintablesize)
	{
		printf("too small");
		return NULL;
	}
	h=malloc(sizeof(struct hashtbl));
	if(h==NULL)
		printf("out of space");
	h->tablesize=NextPrime(2,tablesize);
	/*查找下一个素数*/
	h->thelists=malloc(sizeof(list)*h->tablesize);
	if(h->thelists==NULL)
		printf("out of space");
	for(int i=0;i<h->tablesize;i++)
	{
		h->thelists[i]=malloc(sizeof(struct listnode));
		if(h->thelists[i]==NULL)
			printf("out of space");
		else
			h->thelists[i]->next=NULL;
	}
	return h;
}

position Find(int key, hashtable h)
{
	position p;
	list l;
	l=h->thelists[Hash(key,h->tablesize)];
	p=l->next;
	while(p!=NULL &&p->element!=key)
		p=p->next;
	return p;
}

void Insert(int key, hashtable h)
{
	position pos,newcell;
	list l;
	pos=Find(key, h);
	if (pos==NULL)
	{
		newcell=malloc(sizeof(struct listnode));
		if(newcell==NULL)
			printf("out of space");
		else
		{
			l=h->thelists[Hash(key,h->tablesize)];
			newcell->next=l->next;
			newcell->element=key;
			l->next=newcell;
			/*插入到链表头*/
		}
	}
}
