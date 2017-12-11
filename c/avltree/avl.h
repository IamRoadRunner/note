#ifndel _AvlTree_H
struct avlnode;
typedef struct avlnode *position;
typedef struct avlnode *avltree;

avltree MakeEmpty(avltree t);
position Find(int x,avltree t);
position FindMin(avltree t);
position FindMax(avltree t);
avltree Insert(int x, avltree t);
avltree Delete(int x, avltree t);
int Retrieve(position p);/*检索*/
#endif

struct avlnode
{
	int element;
	avltree left;
	avltree right;
	int height;
};
