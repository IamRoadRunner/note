typedef struct treenode *ptrtonode;
typedef struct treenode tree;
struct treenode
{
	int element;
	ptrtonode firstchild;
	ptrtonode nextsibling;/*兄弟*/
};



/*二叉树*/
sturct treenode
{
	int element;
	tree left;
	tree right;
};