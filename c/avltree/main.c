#include<stdio.h>
#include<stdlib.h>
#include"avl.h"
int main(void)
{
	return 0;
}

static int Height(position p)
{
	if(p==NULL)
		return -1;
	else
		return p->height;
}
int Max(int x,int y)
{
	return x>y?x:y;
}

avltree Insert(int x,avltree t)
{
	if(t==NULL)
	{
		t=malloc(sizeof(struct avlnode));
		if (t==NULL)
			printf("out of space");
		else
		{
			t->element=x;
			t->height=0;
			t->left=t->right=NULL;
		}
	}
	else
		if(x<t->element)
		{
			t->left=Insert(x,t->left);
			if(Height(t->left)-Height(t->right)==2)
				if(x<t->left->element)
					t=SingleRotateWithLeft(t);
				else
					t=DoubleRotateWithLeft(t);
		}
		else if(x>t->element)
		{
			t->right=Insert(x,t->right);
			if(Height(t->right)-Height(t->right)==2)
				if(x<t->right->element)
					t=SingleRotateWithRight(t);
				else
					t=DoubleRotateWithRight(t);
		}
	t->height=Max(Height(t->left),Height(t->right))+1;
	return t;
}
static position
SingRotateWithLeft(position k2)
{
	position k1;
	k1=k2->left;
	k2->left=k1->right;
	k1->right=k2;
	k2->height=Max(Height(k2->left),Height(k2->right))+1;
	k1->height=Max(Height(k1->left),k2->height)+1;
	return k1;
}
