#include<stdio.h>
#include<stdlib.h>
#include"tree.h"
int main(void)
{
	return 0;
}

searchtree MakeEmpty(searchtree t)
{
	if(t!=NULL)
	{
		MakeEmpty(t->left);
		MakeEmpty(t->right);
		free(t);
	}
	return NULL;
}

position Find(int x,searchtree t)
{
	if(t==NULL)/*空树检查*/
		return NULL;
	if(t->element<x)
		/*可以使用goto
		 * t=t->right;
		 * goto Find;*/
		return Find(x,t->right);
	else if(t->element>x)
		return Find(x,t->left);
	else
		return t;
}

position FindMin(searchtree t)
{
	if(t==NULL)
		return NULL;
	else
	if(t->left==NULL)
		return t;
	else
	return FindMin(t->left);	
}

/*FindMax类似*/
searchtree Insert(int x, searchtree t)
{
	if(t==NULL)
	{
		t==malloc(sizeof(struct treenode));
		if(t==NULL)
			printf("out of space");
		else
		{
			t->element=x;
			t->left=t->right=NULL;
		}
	}
	else
		if(x<t->element)
			t->left=Insert(x,t->left);
		else
			if(x>t->element)
				t->right=Insert(x,t->right);
	return t;
}

searchtree Delete(int x, searchtree t)
{
	position tmpcell;
	if(t==NULL)
		printf("not found element");
	else 
		if(x<t->element)
			t->left=Delete(x,t->left);
		else
			if(x>t->element)
				t->right=Delete(x,t->right);
			else
				if(t->left && t->right)
				{
					tmpcell=FindMin(t->right);
					t->element=tmpcell->element;
					t->right=Delete(t->element,t->right);
				}
				else
				{
					if(t->left==NULL)
						t=t->right;
					else if(t->right=NULL)
						t=t->left;
				}
	return t;
}
