/*typedef struct treenode *ptrtonode;
typedef struct treenode tree;
struct treenode
{
	int element;
	ptrtonode firstchild;
	ptrtonode nextsibling;兄弟
};*/
#ifndef _Tree_H


struct treenode;
typedef struct treenode *position;
typedef struct treenode *searchtree;

searchtree MakeEmpty(searchtree t);
position Find(int x,searchtree t);
position FindMin(searchtree t);
position FindMax(searchtree t);
searchtree Insert(int x, searchtree t);
searchtree Delete(int x, searchtree t);
int Retrieve(position p);
#endif 
/*二叉树*/
struct treenode
{
	int element;
	searchtree left;
	searchtree right;
};
